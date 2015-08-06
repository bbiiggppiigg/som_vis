resolvers ++= Seq(
	"Local Maven Repo" at "file://" + Path.userHome.absolutePath+"/.m2/repository")
libraryDependencies ++=Seq(
	"org.encog" % "encog-core" % "3.2.0")


name := "hello"