# Profiles on hold

Profiles in this folder are kept for the record but are **not part of any batch**. `pwatch dq` does not check or count them as batch profiles (it reports them as `cv_profiles_on_hold`), and `pwatch render` neither writes nor checks their markdown. A profile file may also carry `"status": "on_hold"` and a `hold_reason`.

A held profile returns to the batch only through a new change record, once the reason for the hold is resolved.

| Profile | Change | Reason (short) |
|---|---|---|
| MTHEMBENI SELBY MBATHA (MK, ward 61) | CHG-PW-003 fix 1 (17 Nov 2026) | Two councillors surnamed MBATHA in Gazette 55741; no allowed source gives two identifying details for this one |
