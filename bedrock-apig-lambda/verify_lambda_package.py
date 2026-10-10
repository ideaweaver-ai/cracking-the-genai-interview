import pkgutil

def lambda_handler(event, context):

    modules = sorted(
        module.name for module in pkgutil.iter_modules()
    )

    return {
        "statusCode": 200,
        "modules": modules,
        "total_modules": len(modules)
    }
