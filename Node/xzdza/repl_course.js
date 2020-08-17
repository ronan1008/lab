const mongoose = require("mongoose")
const Subscriber = require("./models/subscriber")
const Course = require("./models/course")

var testCourse
var testSubscriber
let mongoDbAtlas = "mongodb+srv://xzdzaorgtw:886229936810@xzdza.elxrf.mongodb.net/xzdza?retryWrites=true&w=majority"
//let mongoDB = "mongodb://localhost:27017/xzdza"

mongoose.connect(mongoDbAtlas,
                    {
                        useNewUrlParser: true,
                        useUnifiedTopology: true,
                        useCreateIndex: true,
                        useFindAndModify: false
                    }
                )
Course.create({
        grade: "2020",
        title: "Tomato Land",
        description: "Locally farmed tomatoes only",
        maxStudents: 12,
        startTime: "2019-08-10 22:23:00",
        endTime: "2019-08-10 22:23:00"
    })
    .then(course => {
        console.log(`Created Course: ${course}`)
    })
    .then(() => {
        return Course.create({
            grade: "2021",
            title: "Apple Land",
            description: "Locally farmed tomatoes only",
            maxStudents: 20,
            startTime: "2019-08-10 22:23:00",
            endTime: "2019-08-10 22:23:00"
        })
    })
    .then(course => {
        console.log(`Created Course: ${course}`)
    })