const mongoose = require("mongoose")
const { Schema } = mongoose

var subscriberSchema = new Schema(
    {
        name:{
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
        courses: [{type: Schema.Types.ObjectId, ref: "Course"}]
    },
    {
        timestamps: true
    }
)

subscriberSchema.methods.getInfo = function () {
    return `Name: ${this.name} Email: ${this.email} Sex: ${this.sex} address: ${this.address} tel: ${this.tel} courses: ${this.courses}`
}

module.exports = mongoose.model("Subscriber", subscriberSchema)