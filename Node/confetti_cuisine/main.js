const express = require('express'),
      app = express(),
      homeController = require("./controllers/homeController"),
      errorController = require("./controllers/errorController"),
      subscribersController = require("./controllers/subscribersController"),
      layouts = require("express-ejs-layouts");
      mongoose = require("mongoose"),
      //Subscriber = require("./models/subscriber");


mongoose.connect("mongodb://localhost:27017/recipe_db",{useNewUrlParser: true})
const db = mongoose.connection
db.once("open",() => {
	console.log("Successfully connected to MongoDB using Mongoose!")
})

// var myQuery = Subscriber.findOne({
//   name: "Jon Wexler"
// }).where("name",/wexler/);

// myQuery.exec((error,data) => {
//   if(data) console.log(data.name)
// });


app.set("view engine", "ejs");
app.set("port", process.env.PORT || 3000)
app.use(express.urlencoded({extended: false}))
app.use(express.json())
app.use(layouts);
app.use(express.static("public"));

app.get("/", (req, res) => {
  res.render("index");
});
app.get("/courses", homeController.showCourses)

app.get("/subscribers", subscribersController.getAllSubscribers)
app.get("/contact",subscribersController.getSubscriptionPage)
app.post("/subscribe",subscribersController.saveSubscriber)

app.use(errorController.pageNotFoundError);
app.use(errorController.internalServerError);

app.listen(app.get("port"), ()=>{
    console.log(`Server running at http://localhost:${app.get('port')}`)
})