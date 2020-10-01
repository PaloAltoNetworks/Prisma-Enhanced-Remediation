"""
Remediate Prisma Policy:

AWS:REDSHIFT-001 Redshift Cluster Is Publicly Accessible

Description:

It is the recommended best practice that Redshift cluster nodes are not accessible to the public internet,
outside of your VPC. This is dangerous, as Redshift databases should normally be privately accessible only
from within your VPC.

Required Permissions:

- redshift:DescribeClusters
- redshift:ModifyCluster

Sample IAM Policy:

{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "RedshiftPermissions",
      "Action": [
        "redshift:DescribeClusters",
        "redshift:ModifyCluster"
      ],
      "Effect": "Allow",
      "Resource": "*"
    }
  ]
}
"""

import boto3
from botocore.exceptions import ClientError


def remediate(session, alert, lambda_context):
  """
  Main Function invoked by index_prisma.py
  """

  cluster_id = alert['resource_id']
  region = alert['region']

  redshift = session.client('redshift', region_name=region)

  try:
    cluster = redshift.describe_clusters(ClusterIdentifier=cluster_id)['Clusters']
  except ClientError as e:
    print(e.response['Error']['Message'])
    return

  try:
    public = cluster[0]['PubliclyAccessible']
  except (KeyError, IndexError):
    public = False

  if public == True: 

    try:
      redshift.modify_cluster(
        ClusterIdentifier = cluster_id,
        PubliclyAccessible = False
      )
    except ClientError as e:
      print(e.response['Error']['Message'])
      return

    else:
      print('Removed public attribute from Redshift cluster {}.'.format(cluster_id))

  return

