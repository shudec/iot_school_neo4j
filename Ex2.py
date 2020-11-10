from InitDB import session

# delete all nodes
session.run("MATCH (n) DETACH DELETE n")

result = session.run("CREATE (ee:Person { name: \"Emil\", from: \"Sweden\", klout: 99 })  RETURN id(ee) AS node_id")
emil = result.single()
print("emil id: {}".format(emil["node_id"]))


result = session.run("MATCH (ee:Person) WHERE ee.name = \"Emil\" RETURN ee;")
ee = result.single()
print("\nemil : {}".format(ee.value()))

req = """MATCH (ee:Person) WHERE ee.name = "Emil"
CREATE (js:Person { name: "Johan", from: "Sweden", learn: "surfing" }),
(ir:Person { name: "Ian", from: "England", title: "author" }),
(rvb:Person { name: "Rik", from: "Belgium", pet: "Orval" }),
(ally:Person { name: "Allison", from: "California", hobby: "surfing" }),
(ee)-[:KNOWS {since: 2001}]->(js),(ee)-[:KNOWS {rating: 5}]->(ir),
(js)-[:KNOWS]->(ir),(js)-[:KNOWS]->(rvb),
(ir)-[:KNOWS]->(js),(ir)-[:KNOWS]->(ally),
(rvb)-[:KNOWS]->(ally)"""
result = session.run(req)

req = """MATCH (ee:Person)-[:KNOWS]-(friends)
WHERE ee.name = "Emil" RETURN ee, friends"""
result = session.run(req)
print("\nfriends of {} : ".format(result.peek()["ee"]))
for r in result:
    print("  - {}".format(r["friends"]))

req= """MATCH (js:Person)-[:KNOWS]-()-[:KNOWS]-(surfer)
WHERE js.name = \"Johan\" AND surfer.hobby = \"surfing\"
RETURN DISTINCT surfer"""
result = session.run(req)
print("\nsurfer : {}".format(result.peek()["surfer"]))