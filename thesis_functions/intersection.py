import numpy as np
import pandas as pd


def get_same_indices(df1, df2):
    m1 = df1.run_start.values.reshape(-1, 1) < df2.run_stop.values.reshape(1, -1)
    m2 = df2.run_start.values.reshape(1, -1) < df1.run_stop.values.reshape(-1, 1)
    return (m1 & m2).nonzero()


def get_better_magic_dateframe(df):
    sls = []
    for run in np.unique(df.run_number):
        _df = df[df.run_number == run]
        if _df.isna().sum().sum() > 0:
            _df = _df.fillna(method="ffill").fillna(method="bfill")
        sl = {
            "night": int(_df.obs_date.values[0].replace("-", "")),
            "run_number": run,
            "run_start": np.array(_df.subrun_start.values, dtype="datetime64[ns]")
            .astype(np.int64)
            .min(),
            "run_stop": np.array(_df.subrun_stop.values, dtype="datetime64[ns]")
            .astype(np.int64)
            .max(),
        }
        sls.append(sl)
    fd = pd.DataFrame(sls)
    return fd


def get_better_fact_dateframe(df):
    fd = pd.DataFrame(
        columns=["night", "run_number", "run_start", "run_stop"], dtype="int64"
    )
    fd["night"] = df.fNight.values
    fd["run_number"] = df.fRunID.values
    fd["run_start"] = df.fRunStart.values.astype(np.int64)
    fd["run_stop"] = df.fRunStop.values.astype(np.int64)
    return fd


def create_united_df(fact, magic):
    df = pd.DataFrame(
        columns=["night_magic", "run_number_magic", "night_fact", "run_number_fact"]
    )
    ind_f, ind_m = get_same_indices(fact, magic)
    df["night_magic"] = magic.iloc[ind_m]["night"].values
    df["night_fact"] = fact.iloc[ind_f]["night"].values
    df["run_number_magic"] = magic.iloc[ind_m]["run_number"].values
    df["run_number_fact"] = fact.iloc[ind_f]["run_number"].values
    # df["run_start_magic"] = magic.iloc[ind_m]["run_start"].values
    # df["run_stop_magic"] = magic.iloc[ind_m]["run_stop"].values
    # df["run_start_fact"] = fact.iloc[ind_f]["run_start"].values
    # df["run_stop_fact"] = fact.iloc[ind_f]["run_stop"].values
    start = np.maximum(fact.iloc[ind_f]["run_start"].values, magic.iloc[ind_m]["run_start"].values)
    # df["start"] = start
    stop = np.minimum(fact.iloc[ind_f]["run_stop"].values, magic.iloc[ind_m]["run_stop"].values)
    # df["stop"] = stop
    df["duration"] = stop - start
    return df
