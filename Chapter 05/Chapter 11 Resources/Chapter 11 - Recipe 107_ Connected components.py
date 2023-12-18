# Databricks notebook source
# based on https://graphframes.github.io/graphframes/docs/_site/user-guide.html#creating-graphframes


# COMMAND ----------

from graphframes.examples import Graphs
g = Graphs(sqlContext).friends() 
display(g.vertices)

# COMMAND ----------

display(g.edges)

# COMMAND ----------

sc.setCheckpointDir("/tmp/graphframes-example-connected-components")
result = g.connectedComponents()
display(result)

# COMMAND ----------


