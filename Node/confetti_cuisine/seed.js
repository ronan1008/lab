const mongoose = require("mongoose"),
	Subscriber = require("./models/subscriber")

//連接到Database
mongoose.connect(
	"mongodb://localhost:27017/recipe_db",
	{ useNewUrlParser: true }
)
mongoose.connection

var contacts = [
	{
		name:"Jon Wexler",
		email: "jon@jonwexler.com",
		zipCode: 10016
	},
	{
		name: "Chef Eggplant",
		email: "eggplant@recipeapp.com",
		zipCode: 20331
	},
	{
		name: "Professor Souffle",
		email: "souffle@recipeapp.com",
		zipCode: 19103
	}
]
//移除現有的資料
Subscriber.deleteMany()
	.exec()
	.then(() => {
		console.log("Subscriber data is empty!")
	})

var commands = []
//迴圈subscriber物件到 create promises
contacts.forEach((c) => {
	commands.push(Subscriber.create({
		name: c.name,
		email: c.email
	}))
})
//Promise.all 等待所有的 new subscriber 被產生
//當 promise resolve 後 紀錄資訊
Promise.all(commands)
	.then( r => {
		console.log(JSON.stringify(r))
		mongoose.connection.close()
	})
	.catch(error => {
		console.log(`ERROR: ${error}`)
	})
