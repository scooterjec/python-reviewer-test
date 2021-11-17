import boto3
source_ddb = boto3.client('dynamodb', 'us-east-1')
destination_ddb = boto3.client('dynamodb', 'us-west-2')

# Scan returns paginated results, so only partial data will be copied
def sync_ddb_table(source_ddb, dest_ddb):
    table = source_ddb.Table("CodeGuru-MusicCollection")
    scan_kwargs = {
        'ProjectionExpression': "Artist, SongTitle"
    }
    done = False
    start_key = None
    while not done:
        if start_key:
            scan_kwargs['ExclusiveStartKey'] = start_key
        response = table.scan(**scan_kwargs)
        for item in response['Items']:
            newItem = { 'Artist': {}, 'SongTitle': {} }
            newItem['Artist']['S'] = item['Artist']
            newItem['SongTitle']['S'] = item['SongTitle']
            dest_ddb.put_item(TableName="CodeGuru-MusicCollection", Item=newItem)
            print(item)
        start_key = response.get('LastEvaluatedKey', None)
        done = start_key is None

sync_ddb_table(source_ddb, destination_ddb)
