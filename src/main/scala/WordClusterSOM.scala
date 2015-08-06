import java.io.File
import java.io.FileWriter
import java.io.PrintWriter

import scala.collection.JavaConversions._
import scala.collection.mutable.ArrayBuffer
import scala.io.Source
import scala.util.Random

import org.encog.mathutil.rbf.RBFEnum
import org.encog.ml.data.basic.BasicMLData
import org.encog.ml.data.basic.BasicMLDataSet
import org.encog.neural.som.SOM
import org.encog.neural.som.training.basic.BasicTrainSOM
import org.encog.neural.som.training.basic.neighborhood.NeighborhoodRBF


case class WordClusterSOM(infile : File, outfile : File,mapSize : Int){
	val words = ArrayBuffer[String]()
	val dataset = new BasicMLDataSet()
	Source.fromFile(infile).getLines().foreach(line =>{
			val cols = line.split(",")
			val word = cols(cols.length-1)
			if(word.length>1){
				val vec = cols.slice(0,cols.length-1).map(e => e.toDouble )
				dataset.add(new BasicMLData(vec))
				words += word	
			}
		})
	val som = new SOM(100,mapSize*mapSize)
	som.reset()
	val neighborhood = new NeighborhoodRBF(RBFEnum.Gaussian,mapSize,mapSize)
	val learningRate = 0.01
	val train = new BasicTrainSOM(som,learningRate,dataset,neighborhood)
	train.setForceWinner(false)
	train.setAutoDecay(1000,0.8,0.003,30,5)
	(0 until 1000).foreach(i=>{
		val idx = (Random.nextDouble * words.size).toInt
		val data = dataset.get(idx).getInput()
		train.trainPattern(data)
		train.autoDecay()
		//Console.println("Epoch %d, Rate : %.3f, Radius: %.3f , Error %.3f".format(i,train.getLearningRate(),train.getNeighborhood().getRadius(),train.getError()))
	})
	
	 /*(0 until 1000).foreach(i => {
	 	Console.println(i)
		train.iteration()
		Console.println(i)
		train.autoDecay()
		Console.println("Epoch %d, Rate: %.3f, Radius: %.3f, Error: %.3f"
	      .format(i, train.getLearningRate(), train.getNeighborhood().getRadius(),
	        train.getError()))
	})*/
	
	val writer = new PrintWriter(new FileWriter(outfile),true)
	dataset.getData().zip(words).foreach(dw=> {
			val xy = convertToXY(som.classify(dw._1.getInput()))
			writer.println("%s\t%d\t%d".format(dw._2,xy._1,xy._2))
		})
	writer.flush()
	writer.close()
	def convertToXY(pos : Int) : (Int,Int) ={
		val x = Math.floor(pos/mapSize).toInt
		val y = pos - (mapSize*x)
		(x,y)
	}
	
}

object Main{
	def main(args: Array[String]) {
	 if(args.length==3)
     	new WordClusterSOM(new File(args(0)),new File(args(1)),args(2).toInt)
     else
     	Console.println("Usage : inputFileName, outputFileName, mapSize ");
    }
}

