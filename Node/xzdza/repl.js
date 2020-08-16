const mongoose = require("mongoose")
const Subscriber = require("./models/subscriber")
const Course = require("./models/course")

var testCourse
var testSubscriber

mongoose.connect("mongodb://localhost:27017/xzdza", 
                    {
                        useNewUrlParser: true,
                        useUnifiedTopology: true,
                        useCreateIndex: true,
                        useFindAndModify: false
                    }
                )


Subscriber.deleteMany({})
	.then((items) => console.log(`Removed ${items.n} records!`))
    .then(() => {
		return Course.deleteMany({})
	})
	.then((items) => console.log(`Removed ${items.n} records!`))
	.then(() => {
		return Subscriber.create({
            name: "Jon",
            email: "jon@jonwexler.com",
            sex: "male",
            address: "新北市",
            tel:"09328323",
		})
	})
	.then(subscriber => {
		console.log(`Created Subscriber: ${subscriber.getInfo()}`)
	})
	.then(() => {
		return Subscriber.findOne({
			name: "Jon"
		})
	})
	.then(subscriber => {
		testSubscriber = subscriber
		console.log(`Found one subscriber: ${ subscriber.getInfo() }`)
	})
	.then(() => {
		return Course.create({
            grade: "2020",
			title: "Tomato Land",
			description: "Locally farmed tomatoes only",
			maxStudents: 12,
            items: ["cherry", "heirloom"],
            startTime: "2019-08-10 22:23:00",
            endTime: "2019-08-10 22:23:00"
		})
	})
	.then(course => {
		testCourse = course
		console.log(`Created course: ${course.title}`)
	})
	.then(() => {
		testSubscriber.courses.push(testCourse)
		testSubscriber.save()
	})
	.then(() => {
		return Subscriber.populate(testSubscriber, "courses")
	})
	.then(subscriber => console.log(subscriber))
	.then(() => {
		return Subscriber.find({ courses: mongoose.Types.ObjectId(testCourse._id) })
	})
    .then(subscriber => console.log(subscriber))
    
