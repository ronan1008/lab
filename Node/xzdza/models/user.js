const mongoose = require("mongoose")
const { Schema } = require("mongoose")
const Subscriber = require("./subscriber")
//const passportLocalMongoose = require("passport-local-mongoose")
const bcrypt = require("bcrypt")
const userSchema = new Schema(
    {
        name:{
            type: String,
            required: true,
            trim: true
        },
        loginId:{
            type: String,
            required: true,
            trim: true
        },
        email: {
            type: String,
            required: true,
            lowercase: true,
            trim: true,
            unique: true

        },
        sex: {
            type: String,
            required: true,
            enum : ['male','female','unisex'],
        },
        address: {
            type: String,
            required: true,
        },
        tel: {
            type: String,
            required: true,
        },
        password: {
            type: String,
            required: true
        },
        role:{
            type: String,
            required: true,
            enum : ['admin','user']
        }
    },
    {
        timestamps: true
    }
)


userSchema.pre("save", function(next){
    let user = this
    bcrypt.hash(user.password, 10)
        .then(hash => {
            user.password = hash
            next()
        })
        .catch(error => {
            console.log(`Error in hash password ${error.message}`)
            next(error)

        })
})

userSchema.methods.passwordComparison = function(inputPassword){
    let user = this
    return bcrypt.compare(inputPassword, user.password)
}

// userSchema.plugin(passportLocalMongoose,{ usernameField: "email" })

module.exports = mongoose.model("User", userSchema)