
def extend_results(base_dict, value_for_update):
    """Update result dict with a nested dict."""
    for k, v in value_for_update.iteritems():
        if isinstance(v, dict):
            base_dict[k] = extend_results(
                base_dict.get(k, dict()), v
            )
        else:
            base_dict[k] = v
    return base_dict
