const router = require("express").Router()
const coursesController = require("../../controllers/coursesController")

router.get("/", coursesController.index,
                       coursesController.filterUserCourses,
                       coursesController.respondJSON
)

router.post("/:id/join", coursesController.join,coursesController.respondJSON)

router.use(coursesController.errorJSON)

module.exports = router
