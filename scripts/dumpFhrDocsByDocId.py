import jydoop

'''
in following commands, UPDATE DATES

make ARGS="scripts/dumpFhrDocsByDocId.py ./outData/PATH_ON_PEACH_TO_DUMP_TO ./PATH_ON_HDFS_TO_DUMP" hadoop

'''


setupjob = jydoop.setupjob


docIdList = ['0dbc76b1-c8ee-4663-a65e-460fce52d147', '9dffbf88-4eab-4ae6-a74c-160e0b1b2475', '319a0448-ea83-4394-b190-f5180fe2bd7e', '83966a5e-9f86-468e-90bc-40f1b6baba91', 'a7692b1c-ada8-4c75-8235-960e56ddd245', '1fc82142-de51-4cfe-a708-b3e4a4125a89', '367b0331-c4cc-4bfa-a78a-cddd60a729ad', 'e319a141-0037-4358-9bbb-2c8a10f0c5f3', 'ab63283a-f8ca-4c4c-bbec-0dec6d7b49f6', '72509a10-a93c-432a-8c04-225868c3551b', 'fd6f8e00-721e-4daa-80ca-9922f8a58bcc', '3407876b-4773-4ef5-a5cd-b899df251039', '66a02ab7-30a9-4034-9239-3858f57c0ad6', 'a1f5e846-2b05-49a4-9452-373b2fe9434d', 'f3c95ff2-6b87-4ebd-9c71-62dc6a04f6f7', '8707ae27-b4b1-4959-ad74-2841b2f2c01e', '09f92abb-cc9a-4eb7-9451-d5c8b12144fc', '5d507fa0-91f5-4602-9164-2e99405ddbdb', 'f6985da8-f6c1-4757-9ed5-19c05e7a01e2', '8dc3c757-7eb0-48fb-9dc2-c052d4e8f3a0', 'd821ec9b-3d70-49ba-bd2f-422ffa39e68c', 'cf94893a-cb3d-4e09-aaf5-9b0cda032c40', '5965ac76-24a7-4364-9229-6740203621d1', 'b5705f1c-3f83-4d54-bda6-5fd1da5e5cf7', 'e3e1a5e4-7f94-4ca2-9123-41943c6ade78', 'fac829e7-86f3-4204-8738-d3cd818d7543', '83dfbd13-998d-4b07-9bd6-79153d7e9cf5', '88f61e67-ea2f-40fa-9090-942aa2967351', '9f79b5d3-e4f6-485f-90d9-454a9381df04', '69dd269d-1b31-4fec-9cc8-ea081cddb9c2']
# ['1414e149-ec80-4795-ae0f-08e7b30ae8d6', '305b8723-5d17-44df-b3e1-9231b998b906', '40753e99-3227-4c78-943a-3bfb10753157', '4329d275-391f-4f31-87a4-4633f175293c', 'b4af172a-6762-41e2-a6e1-34929a8bfb3e', '5254e667-6824-4584-a678-db4cd2ed9216', '8c943f22-5bff-49dd-b2d4-7ddd6d99e579', 'c0a896b0-91da-495a-9001-88bbf1c25440', '0adb5f36-d8a2-47d0-add9-3a0583f400b0', 'ebe4e647-1ad0-419d-9aa4-d2a907b45d08', 'a7d81bda-47e4-4147-b175-715e38c0e2c2', '47aba0b5-3a22-42d4-8162-fe078bbd7a4b', 'd63d4e24-03f4-4923-9aa3-672a7f817cc2', '85298150-d01b-4247-a52e-797d3d9fa7cb', '9a8a068e-1dbe-455f-964b-2f2c43f71d12', 'a646facf-31d3-47d5-b224-4e820a4827b4', '99a86ce5-7de0-4d55-9ef1-0103c4fa9c5b', '8b221a60-bc13-4a59-9c91-2091d95f45fa', '2d6ea8fd-bf30-405c-bbc5-75ba03a9d6fd', 'bf78d07b-205d-4288-9a1f-68defd65c52c', '2e9a9015-b576-41bd-92a0-ddd5d57227fc', 'e8cc87ea-4832-4b57-873d-6128b2c743f5', '965307b9-a932-4771-b429-bea02f297861', '6214bdff-b441-42b7-b858-ce91529138eb', '404c9e6a-072c-4562-aae5-9cdc7ee8b8ad', 'b16f10bd-92f0-40d2-8574-00a8be34de42', '5c36b3a7-39de-4ee6-8a03-8ec5718b6d0e', 'ccf7143a-4bbd-44a5-9b1d-1bbce71a0f1b', 'bb70c58c-c614-49f7-ab07-87caf6ab740c', '483683bf-e98a-411f-a66a-37a77dec84a3', 'e50e5d51-6573-447b-9e22-acf60e848861']



def output(path, results):
    # just dump tab separated key/vals
    f = open(path, 'w')
    for k, v in results:
        print >>f, str(v)



def map(key,val,context):
    if key in docIdList:
        context.write(str(key),str(val))