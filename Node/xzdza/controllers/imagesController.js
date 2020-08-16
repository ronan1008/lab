const Image = require("../models/image")
const httpStatus = require('http-status-codes')
const path = require('path');
const sizeOf = require('image-size');
module.exports = {
    upload: (req, res, next) => {
        let image = req.files.image
        imagePath = path.resolve(__dirname,'../public/images',image.name)
        image.mv(imagePath,(error)=> {
            let urlPath = `http://localhost:3000/images/${image.name}`
            Image.create({'path': urlPath})
                .then(images => {
                    let dimensions = sizeOf(imagePath)
                    image ={
                        data: [
                            urlPath,
                            {
                              src: urlPath,
                              type: 'image',
                              height: dimensions.height,
                              width: dimensions.width,
                            },
                        ]
                    }
                    res.json(image)
                })
                .catch(error => {
                    console.log(`Error saving news: ${error.message}`)
                    next(error)
                })
        })
    },

    delete: (req, res, next) => {
        let imageId = req.params.id 
        News.findByIdAndRemove(imageId)
            .then(() => {
                res.locals.redirect = "/news"
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

}