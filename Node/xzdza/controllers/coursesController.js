const Course = require("../models/course")
const Subscriber = require("../models/subscriber")
const httpStatus = require('http-status-codes')
const getCourseParams = body => {
    return {
        title : body.title,
        description: body.description,
        grade: body.grade,
        maxStudents: body.maxStudents,
        startTime: body.startTime,
        endTime: body.endTime
    }
}
module.exports = {
    index: (req, res, next) => {
        Course.find()
            .then(courses => {
                //courses.subscribers = courses.subscribers.length
                res.locals.courses = courses
                next()
            })
            .catch(error => {
                console.log(`Error fetching courses: ${error.message}`)
                next(error)
            })
    },

    frontIndex: (req, res, next) => {
        Course.find({
           "startTime": {$lte:  new Date()},
           "endTime": {$gte:  new Date()}
        })
        .then(courses => {
            //courses.subscribers = courses.subscribers.length
            res.locals.courses = courses
            next()
        })
        .catch(error => {
            console.log(`Error fetching courses: ${error.message}`)
            next(error)
        })
    },

    filterCourse: (req, res, next) => {
        //console.log(res.locals.news)
        let filterCourse = res.locals.courses.map(( course =>{
            var courseList = {}
            courseList['_id'] = course._id
            courseList['grade'] = course.grade
            courseList['title'] = course.title
            courseList['maxStudents'] = course.maxStudents
            courseList['subscribers'] = course.subscribers.length
            courseList['startTime'] = course.startTime
            courseList['endTime'] = course.endTime
            return courseList;
        }))
        res.locals.courses = filterCourse
        next()
    },

    create: (req, res, next) => {
        let courseParams = getCourseParams(req.body)
        Course.create(courseParams)
            .then(course => {
                res.locals.course = course
                next()
            })
            .catch(error => {
                console.log(`Error saving course: ${error.message}`)
                next(error)
            })
    },

    show: (req, res, next) => {
        let courseId = req.params.id
        Course.findById(courseId)
            .then(course => {
                return Course.populate(course, "subscribers")
            })
            .then( (course) => {
                res.locals.course = course
                next()
            })
            .catch(error => {
                console.log(`Error fetching course by ID: ${error.message}`)
                next(error)
            })
    },

    update: (req, res, next) => {
        let courseId = req.params.id
        courseParams = getCourseParams(req.body)
        Course.findByIdAndUpdate(courseId,{ $set: courseParams})
            .then(course => {
                res.locals.course = course
                next()
            })
            .catch(error => {
                console.log(`Error updating course by ID : ${error.message}`)
                next(error)
            })
    },

    delete: (req, res, next) => {
        let courseId = req.params.id
        Course.findByIdAndRemove(courseId)
            .then( () => {
                res.locals.course = courseId
                next()
            })
            .catch(error => {
                console.log(`Error course by ID: ${error.message}`)
                next()
            })
    },

    respondJSON: (req, res) => {
        res.json({
            status: httpStatus.OK,
            data: res.locals,
            message: 'Ok'
        })
    },

    errorJSON: (error, req, res, next) => {
        let errorObject
        if (error) {
            console.log(error.message)
            if (error.message.indexOf('You have already signed') != -1){
                errorObject = {
                    status: httpStatus.FORBIDDEN,
                    message: error.message
                }
            } else {
                errorObject = {
                    status: httpStatus.INTERNAL_SERVER_ERROR,
                    message: error.message
                }
            }
        } else {
            errorObject = {
                status: httpStatus.OK,
                message: "Unknown Error."
            }
        }
        res.json(errorObject)
    },

    filterUserCourses: (req, res, next) => {
        let currentUser = res.locals.currentUser
        if ( currentUser ) {
            let mappedCourses = res.locals.courses.map((course => {
                let userJoined = currentUser.courses.some((userCourse) => {
                    return userCourse.equals(course._id)
                })
                return Object.assign(course.toObject(), {joined: userJoined})
            }))
            res.locals.courses = mappedCourses
            next()
        } else {
            next()
        }
    },
//TODO:
    join:  (req, res, next) => {
        var joinSubcriber
        var joinCourse
        let courseId = req.params.id
        userJson = {
            title: req.body.title,
            address: req.body.address,
            email: req.body.email,
            birthday: new Date(req.body.birthday),
            name: req.body.name,
            sex: req.body.sex,
            tel: req.body.tel,
            zodiac: req.body.zodiac
        }
        Course.findById(courseId).populate({path:'subscribers', select: 'email'})
            .then(courses => {
                // courses.subscribers.map((subscriber)=>{
                //     console.log(subscriber)
                //     if (subscriber.email == req.body.email){                   
                //         throw new Error("You have already signed")
                //     }
                var findEmail = courses.subscribers.find(function(item, index, array){
                        return item.email == req.body.email;  
                });
                if(findEmail) {throw new Error("You have already signed")}



                // })
            }) 
            .then(() => {
                return Subscriber.create(userJson)
            })

            .then(subscriber => {
                joinSubcriber = subscriber
                console.log(`Created Subscriber: ${subscriber.getInfo()}`)
            })
            .then(() => {
                return Course.findById(courseId).select('_id title grade subscribers maxStudents')
            })
            .then((course) => {
                if (course.subscribers.length < course.maxStudents){
                    joinCourse = course
                    console.log(`Find Course: ${course.title}, Join people: ${course.subscribers.length}`)
                }else{
                    throw new Error("echelon full up")
                }
            })
            .then(() => {
                console.log(joinCourse)
                joinCourse.subscribers.push(joinSubcriber)
                return joinCourse.save()
            })
            .then(() => {
                return Course.populate(joinCourse, { path: 'subscribers', model: 'Subscriber', select: 'name' })
                //return Course.findById(courseId)
            })
            .then(course => {
                console.log(course)
                res.locals.course = course
                next()
            })
            .catch(error => {
                console.log(`Error occur`)
                next(error)
            })

    }
}