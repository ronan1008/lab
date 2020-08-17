const router = require("express").Router()
const coursesController = require("../../controllers/coursesController")

router.get("/", coursesController.frontIndex,coursesController.filterCourse,coursesController.respondJSON)
router.post("/:id/join", coursesController.join)
router.use(coursesController.errorJSON)

module.exports = router
