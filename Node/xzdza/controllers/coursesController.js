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
                courses.subscribers = courses.subscribers.length
                res.locals.courses = courses
                next()           
            })
            .catch(error => {
                console.log(`Error fetching courses: ${error.message}`)
                next(error)
            })
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
                res.locals.redirect =  `/courses/${courseId}`
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
                res.locals.redirect = "/courses"
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
            errorObject = {
                status: httpStatus.INTERNAL_SERVER_ERROR,
                message: error.message
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

    join: (req, res, next) => {
        let courseId = req.params.id
        let currentUser = req.user
        if (currentUSer) {
            User.findByIdAndUpdate(currentUser, {
                $addToSet:{
                    courses: courseId
                }
            })
                .then(() => {
                    res.locals.success = true
                    next()
                })
                .catch((error) => {
                    next(error)
                })
        } else {
            next(new Error("User must log in."))
        }
    },

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
        Subscriber.create(userJson)
            .then(subscriber => {
                joinSubcriber = subscriber
                console.log(`Created Subscriber: ${subscriber.getInfo()}`)
            })
            .then(() => {
                return Course.findById(courseId)
            })
            .then((course) => {
                if (course.subscribers.length < course.maxStudents){
                    joinCourse = course
                    console.log(`Find Course: ${course.title}, Join people: ${course.subscribers.length}`)
                }else{
                    res.json({
                        status: httpStatus.OK,
                        message: "Failed : 名額已滿，沒有加入成功"
                    })
                }
            })
            .then(() => {
                joinCourse.subscribers.push(joinSubcriber)
                joinCourse.save()
            })
            .then(() => {
                return Course.populate(joinCourse, "subscribers")
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