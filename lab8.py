import base64
import boto3
import json
import os
import sys

bucketname = '21664707-cloudstorage1'
schema = 'banking.csv.schema'
recipe = 'recipe.json'
TRAINING_DATA_S3_URL = "s3://aml-sample-data/banking.csv"


def build_model(data_s3_url, schema_fn, recipe_fn, name, train_percent=70):
    ml = boto3.client('machinelearning')
    (train_ds_id, test_ds_id) = create_data_sources(ml, data_s3_url, schema_fn,train_percent,name)
    ml_model_id = create_model(ml, train_ds_id, recipe_fn, name)
    eval_id = create_evaluation(ml, ml_model_id, test_ds_id, name)

    return ml_model_id


def create_data_sources(ml, data_s3_url, schema_fn, train_percent, name):
    train_ds_id='21664707_train_1'
    spec = {
        "DataLocationS3": data_s3_url,
        "DataRearrangement": json.dumps({
            "splitting": {
                "percentBegin": 0,
                "percentEnd": train_percent
            }
        }),
        "DataSchemaLocationS3": 's3://'+bucketname+'/'+schema,
    }
    ml.create_data_source_from_s3(
        DataSourceId=train_ds_id,
        DataSpec=spec,
        DataSourceName=name + " - training split",
        ComputeStatistics=True
    )
    print("Created training data set %s" % train_ds_id)

    test_ds_id = '21664707_test_2'
    spec['DataRearrangement'] = json.dumps({
        "splitting": {
            "percentBegin": train_percent,
            "percentEnd": 100
        }
    })
    ml.create_data_source_from_s3(
        DataSourceId=test_ds_id,
        DataSpec=spec,
        DataSourceName=name + " - testing split",
        ComputeStatistics=True
    )
    print("Created test data set %s" % test_ds_id)
    return (train_ds_id, test_ds_id)


def create_model(ml, train_ds_id, recipe_fn, name):
    """Creates an ML Model object
    """
    model_id = '21664707_model_1'
    ml.create_ml_model(
        MLModelId=model_id,
        MLModelName=name + " model",
        MLModelType="BINARY",  # predicting True/False values
        Parameters={
            "sgd.maxPasses": "100",
            "sgd.maxMLModelSizeInBytes": "104857600",  # 100 MiB
            "sgd.l2RegularizationAmount": "1e-4",},
        TrainingDataSourceId=train_ds_id
    )
    print("Created ML Model %s" % model_id)
    return model_id


def create_evaluation(ml, model_id, test_ds_id, name):
    eval_id = '21664707_eval_1'
    ml.create_evaluation(
        EvaluationId=eval_id,
        EvaluationName=name + " evaluation",
        MLModelId=model_id,
        EvaluationDataSourceId=test_ds_id
    )
    print("Created Evaluation %s" % eval_id)
    return eval_id


if __name__ == "__main__":
    try:
        data_s3_url = TRAINING_DATA_S3_URL
        schema_fn = "banking.csv.schema"
        recipe_fn = "recipe.json"
        if len(sys.argv) > 2:
            name = sys.argv[1]
        else:
            name = "21664707 Banking"
    except:
        raise
    model_id = build_model(data_s3_url, schema_fn, recipe_fn, name=name)
   
