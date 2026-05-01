def safe_call(model_func, *args, **kwargs):
    try:
        return model_func(*args, **kwargs)
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "response": None,
            "metadata": {}
        }