# bigdl reqs: https://bigdl-project.github.io/0.10.0/#PythonUserGuide/install-from-pip/
#   - Python 2.7, Python 3.5 and Python 3.6; Python 3.6 is only compatible with Spark 1.6.4, 2.0.3, 2.1.1 and 2.2.0
#   - based on this, I'll install python 3.5
# bigdl tutorial: https://github.com/intel-analytics/BigDL-Tutorials/blob/master/notebooks/spark_basics/DataFrame.ipynb

# python version: 3.7.4
# spark version: 3.0.0-preview2

from pyspark import SparkContext
#from bigdl.util.common import *
from pyspark.sql import SparkSession

sc = SparkContext('local')
spark = SparkSession(sc)
sc.version

# Defines a Python list storing one JSON object.
json_strings = ['{"name":"Bob","address":{"city":"Los Angeles","state":"California"}}', ]
# Defines an RDD from the Python list.
peopleRDD = sc.parallelize(json_strings)
# Creates an DataFrame from an RDD[String].
people = spark.read.json(peopleRDD)
people.show()