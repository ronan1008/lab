const News = require("../models/news")
const httpStatus = require('http-status-codes')
const getNewsParams = body => {
    return {
        title : body.title,
        description: body.description,
        type: body.type,
        mark: body.mark,
        order: body.order,
        startTime: body.startTime,
        endTime: body.endTime

    }
}

module.exports = {
    index: (req, res, next) => {
        let query = {}
        if(req.query.type) query.type = req.query.type;
        News.find(query).sort({type:'asc',order:'asc', updatedAt:'desc'})
            .then(news => {
                res.locals.news = news
                next()
            })
            .catch(error => {
                console.log(`Error fetching news: ${error.message}`)
            })
    },

    filterNews: (req, res, next) => {
        //console.log(res.locals.news)
        let filterNews = res.locals.news.map(( news =>{
            var newsList = {}
            newsList['title'] = (news.title.length >= 10) ? `${news.title.substr(1,20)}...`: news.title
            newsList['description'] = (news.description.length >= 20) ? `${news.description.substr(1,20)}...`: news.title
            newsList['_id'] = news._id
            newsList['type'] = news.type
            newsList['order'] = news.order
            newsList['mark'] = news.mark
            newsList['startTime'] = news.startTime
            newsList['endTime'] = news.endTime
            return newsList;
        }))
        res.locals.news = filterNews
        next()
    },

    create: (req, res, next) => {
        let newsParams = getNewsParams(req.body)
        News.create(newsParams)
            .then(news => {
                res.locals.news = news
                next()
            })
            .catch(error => {
                console.log(`Error saving news: ${error.message}`)
                next(error)
            })
    },

    show: (req, res, next) => {
        var newsId = req.params.id 
        News.findById(newsId)
            .then(news => {
                res.locals.news = news
                next()
            })
            .catch(error => {
                console.log(`Error fetching subscriber by ID: ${error.message}`)
                next(error)
            })
    },

    update: (req, res, next) => {
        let newsId = req.params.id 
        let newsParams = getNewsParams(req.body)
        console.log(newsId)
        News.findByIdAndUpdate(newsId, {
            $set : newsParams
        })
            .then(news => {
                //res.locals.redirect = `news/${newsId}`
                res.locals.news = news
                next()
            })
            .catch( error => {
                console.log(`Error updating news by ID: ${error.message}`)
                next(error)
            })
    },

    delete: (req, res, next) => {
        let newsId = req.params.id 
        News.findByIdAndRemove(newsId)
            .then(() => {
                res.locals.news = newsId
                next()
            })
            .catch(error => {
                console.log(`Error deleting subscriber by ID: ${error.message}`)
                next()
            })
    },

    respondJSON: (req, res) => {
        res.json({
            status: httpStatus.OK,
            data: res.locals,
            message: "Ok"
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

}