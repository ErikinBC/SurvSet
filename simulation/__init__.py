"""
Contains the support parameters and functions used by the simulation module.

# To call a test of the main functions run
>>> python3 -m simulation.__init__
"""

# Modules
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sksurv.metrics import concordance_index_censored as concordance


def stratified_group_split(df: pd.DataFrame, 
                           group_col: str ='pid', 
                           stratify_col: str ='event', 
                           test_frac: float = 0.2, 
                           seed: int | None = None):
    '''
    Function to make sure that patient IDs don't show up in both training and test sets. And then also balance the event rate across the two sets.
    '''
    # Step 1: Collapse to group-level (one row per patient)
    group_df = df.groupby(group_col)[stratify_col].any().astype(int).reset_index()
    # Step 2: Stratified split on the group level
    group_train, group_test = train_test_split(
        group_df,
        stratify=group_df[stratify_col],
        test_size=test_frac,
        random_state=seed
    )
    # Step 3: Merge back to original data
    df_train = df[df[group_col].isin(group_train[group_col])]
    df_test = df[df[group_col].isin(group_test[group_col])]
    return df_train, df_test


def bootstrap_concordance_index(
    df: pd.DataFrame,
    id_col: str = "id",
    event_col: str = "event",
    time_col: str = "time",
    score_col: str = "score",
    time2_col: str | None = None,
    n_bs: int = 1000,
    alpha: float = 0.05,
    is_td: bool = False,
    ) -> pd.DataFrame:
    """
    Wrapper on the concordance_index_timevarying function to perform bootstrap resampling for confidence intervals.
    """
    # Input checks
    expected_cols = [id_col, event_col, time_col, score_col]
    if is_td:
        expected_cols.append(time2_col)
    missing_cols = np.setdiff1d(expected_cols, df.columns)
    assert len(missing_cols) == 0, f"Missing required columns: {missing_cols.tolist()}"
    assert isinstance(n_bs, int) and n_bs > 0, "n_bs must be a positive integer."
    assert 0 < alpha < 1, "alpha must be between 0 and 1."
    assert is_td in [True, False], "is_td must be a boolean value."
    # Subset to only the required columns
    df = df[expected_cols].copy()
    # Set up the storage holder and final DataFrame slice
    holder_bs = np.zeros(n_bs)
    # Get baseline result and then loop over the bootstrap samples
    if is_td:
        # Baseline
        conc_test = concordance_index_timevarying(df, id_col, time_col, time2_col, event_col, score_col)
        # Bootstrap
        for j in range(n_bs):
            res_bs = df.groupby(event_col).sample(frac=1,replace=True,random_state=j)
            conc_bs = concordance_index_timevarying(res_bs, id_col, time_col, time2_col, event_col, score_col)
            holder_bs[j] = conc_bs
    else:
        # Baseline
        conc_test = concordance(df[event_col].astype(bool), df[time_col], df[score_col])[0]
        # Bootstrap
        for j in range(n_bs):
            res_bs = df.groupby(event_col).sample(frac=1,replace=True,random_state=j)
            conc_bs = concordance(res_bs[event_col].astype(bool), res_bs[time_col], res_bs[score_col])[0]
            holder_bs[j] = conc_bs
    # Add on the baseline result and empirical confidence intervals
    lb, ub = np.quantile(holder_bs, [alpha,1-alpha])
    holder_cindex = pd.DataFrame(np.atleast_2d((conc_test, lb, ub)), columns=['cindex', 'lb', 'ub'])
    return holder_cindex



def concordance_index_timevarying(df: pd.DataFrame, 
                                       id_col: str = "id", 
                                       start_col: str = "start", 
                                       stop_col: str = "stop",
                                       event_col: str = "event", 
                                       score_col: str = "score"):
    """
    Fast vectorized calculation of Harrell's C-index for survival data with time-varying covariates.
    
    Parameters:
    - df: DataFrame in counting process format
    - id_col: column identifying subjects
    - start_col: column with interval start times
    - stop_col: column with interval stop times
    - event_col: column indicating if event occurred at 'stop' time (1=event, 0=censor)
    - score_col: column with risk score (higher = higher risk)
    
    Returns:
    - concordance index (float)
    """
    df = df[[id_col, start_col, stop_col, event_col, score_col]].copy()
    df = df.sort_values(by=[stop_col])
    
    # Get events
    events = df[df[event_col] == 1].copy()
    if len(events) == 0:
        return None
    
    # Convert to numpy arrays for faster operations
    event_times = events[stop_col].values
    event_ids = events[id_col].values
    event_scores = events[score_col].values
    
    df_start = df[start_col].values
    df_stop = df[stop_col].values
    df_ids = df[id_col].values
    df_scores = df[score_col].values
    
    concordant = 0
    discordant = 0
    tied_risk = 0
    comparable = 0
    
    # Process events in batches for better memory efficiency
    for i, (t_event, id_event, risk_event) in enumerate(zip(event_times, event_ids, event_scores)):
        # Vectorized risk set identification
        at_risk_mask = (df_start < t_event) & (df_stop >= t_event)
        
        # Get risk set data
        risk_set_ids = df_ids[at_risk_mask]
        risk_set_scores = df_scores[at_risk_mask]
        
        # Remove self-comparisons
        self_mask = risk_set_ids != id_event
        risk_set_scores = risk_set_scores[self_mask]
        
        if len(risk_set_scores) == 0:
            continue
        
        # Vectorized comparisons
        n_risk = len(risk_set_scores)
        concordant += np.sum(risk_event > risk_set_scores)
        discordant += np.sum(risk_event < risk_set_scores)
        tied_risk += np.sum(risk_event == risk_set_scores)
        comparable += n_risk
    
    if comparable == 0:
        return None
    
    return (concordant + 0.5 * tied_risk) / comparable



if __name__ == '__main__':
    # In this first dataset, the concordance is 100% b/c from [0,3) 0.5 > 0.2, and then from [3, 5) there is no event, and then from [5, 10) 0.8 > 0.6.
    test_data1 = pd.DataFrame({
        'id': [1, 1, 2, 2],
        'start': [0, 5, 0, 3],
        'stop': [5, 10, 3, 12],
        'event': [0, 1, 1, 0],
        'score': [0.2, 0.8, 0.5, 0.6]
    })
    # Calculate the concordance index
    c_index1 = concordance_index_timevarying(test_data1, )
    print(f"Concordance Index: {c_index1:.2%} (expected 100%)")
    # In the second example, the concordance will be 0% 
    test_data2 = pd.DataFrame({
        'id': [1, 1, 2, 2],
        'start': [0, 5, 0, 3],
        'stop': [5, 10, 3, 12],
        'event': [0, 1, 1, 0],
        'score': [0.6, 0.8, 0.5, 0.9]
    })
    c_index2 = concordance_index_timevarying(test_data2)
    print(f"Concordance Index: {c_index2:.2%} (expected 0%)")
    # In the third example, it gets the first half right, but the second half wrong
    test_data3 = pd.DataFrame({
        'id': [1, 1, 2, 2],
        'start': [0, 5, 0, 3],
        'stop': [5, 10, 3, 12],
        'event': [0, 1, 1, 0],
        'score': [0.4, 0.8, 0.5, 0.9]
    })
    c_index3 = concordance_index_timevarying(test_data3)
    print(f"Concordance Index: {c_index3:.2%} (expected 50%)")
    # In the fourth example, it gets the first half wrong, but the second half right
    test_data4 = pd.DataFrame({
        'id': [1, 1, 2, 2],
        'start': [0, 5, 0, 3],
        'stop': [5, 10, 3, 12],
        'event': [0, 1, 1, 0],
        'score': [0.4, 0.8, 0.3, 0.7]
    })
    c_index4 = concordance_index_timevarying(test_data3)
    print(f"Concordance Index: {c_index4:.2%} (expected 50%)")
