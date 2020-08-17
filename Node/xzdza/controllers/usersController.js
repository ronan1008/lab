const User = require("../models/user")
const passport = require("passport")
const jsonWebToken = require("jsonwebtoken")
const httpStatus = require('http-status-codes')

getUserParams = body => {
    return {
        name: {
            first: body.first,
            last: body.last
        },
        email: body.email,
        //password: body.password,
        zipCode: body.zipCode
    };
};

module.exports = {
  index: (req, res, next) => {
    User.find()
      .then(users => {
        res.locals.users = users;
        next();
      })
      .catch(error => {
        console.log(`Error fetching users: ${error.message}`);
        next(error);
      });
  },
  indexView: (req, res) => {
    res.render("users/index");
  },

  new: (req, res) => {
    res.render("users/new");
  },

  create: (req, res, next) => {
    if (req.skip) next()
    let newUser = new User(getUserParams(req.body))

    User.register(newUser, req.body.password, (e, user) => {
        if (user) {
            req.flash("success", `${user.fullName}'s account created successfully`)
            res.locals.redirect = "/users"
            next()
        } else {
            req.flash("error", `Failed to create user account because: ${e.message}.`)
            res.locals.redirect = "/users/new"
            next()
        }
    })
  },

  redirectView: (req, res, next) => {
    let redirectPath = res.locals.redirect;
    if (redirectPath !== undefined) res.redirect(redirectPath);
    else next();
  },

  show: (req, res, next) => {
    let userId = req.params.id;
    User.findById(userId)
      .then(user => {
        res.locals.user = user;
        next();
      })
      .catch(error => {
        console.log(`Error fetching user by ID: ${error.message}`);
        next(error);
      });
  },

  showView: (req, res) => {
    res.render("users/show");
  },

  edit: (req, res, next) => {
    let userId = req.params.id;
    User.findById(userId)
      .then(user => {
        res.render("users/edit", {
          user: user
        });
      })
      .catch(error => {
        console.log(`Error fetching user by ID: ${error.message}`);
        next(error);
      });
  },

  update: (req, res, next) => {
    let userId = req.params.id,
      userParams = getUserParams(req.body);

    User.findByIdAndUpdate(userId, {
      $set: userParams
    })
      .then(user => {
        res.locals.redirect = `/users/${userId}`;
        res.locals.user = user;
        next();
      })
      .catch(error => {
        console.log(`Error updating user by ID: ${error.message}`);
        next(error);
      });
  },

  delete: (req, res, next) => {
    let userId = req.params.id;
    User.findByIdAndRemove(userId)
      .then(() => {
        res.locals.redirect = "/users";
        next();
      })
      .catch(error => {
        console.log(`Error deleting user by ID: ${error.message}`);
        next();
      });
  },

  validate: (req, res, next) => {
      req.sanitizeBody("email")
         .normalizeEmail({all_lowercase: true})
         .trim()
      req.check("email", "Email is invalid").isEmail()
      req.check("zipCode", "Zip code is invalid")
         .notEmpty()
         .isInt()
         .isLength({min: 5, max: 5})
         .equals(req.body.zipCode)
      req.check("password", "Password cannot be empty").notEmpty()
      req.getValidationResult().then( (error) => {
          if (!error.isEmpty()){
              let messages = error.array().map(e => e.msg)
              req.skip = true
              req.flash("error", messages.join(" and "))
              res.locals.redirect = "/users/new"
              next()
          } else {
              next()
          }
      })
  },

  // authenticate: passport.authenticate("local", {
  //     failureRedirect: "/users/login",
  //     failureFlash: "Failed to login",
  //     successRedirect: "/",
  //     successFlash: "Logged in!"
  // }),

  apiAuthenticate: (req, res, next) => {
    User.findOne({loginId: req.body.loginId})
        .then(user => {
          console.log(user)
          if (user && user.role == 'admin'){
            user.passwordComparison(req.body.password).then(passwordsMatch => {
              if(passwordsMatch) {
                let signedToken = jsonWebToken.sign(
                  {
                    data: user._id,
                    exp: new Date().setDate(new Date().getDate() + 1 )
                  },
                  "xzdza"
                )
                res.json({
                  status: httpStatus.OK,
                  message: "Ok",
                  data: {token:signedToken}
                })
          
              } else {
                res.status(httpStatus.UNAUTHORIZED).json({
                  error: true,
                  message: "Could not authenticate user."
                })
              }
          
            })
          } else {
            res.status(httpStatus.UNAUTHORIZED).json({
              error: true,
              message: "Error failed to log in: User account not found."
            })
          }
        })
        .catch(error => {
          res.status(httpStatus.UNAUTHORIZED).json({
            error: true,
            message: `Error logging in user: ${error.message}`
          })
        })
  },

  logout: (req, res, next) => {
      req.logout()
      req.flash("success", "You have been logged out!")
      res.locals.redirect = "/"
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

  verifyJWT: (req, res, next) => {
    let token = req.headers.token
    if (token) {
      jsonWebToken.verify(token,"xzdza",(errors, payload) => {
        console.log(payload)
        if (payload){
          User.findById(payload.data).then( user => {
            if (user && user.role=='admin') {
              next()
            } else {
              res.status(httpStatus.FORBIDDEN).json({
                error: true,
                message: "No User account found."
              })
            }
          })
        } else {
          res.status(httpStatus.UNAUTHORIZED).json({
            error: true,
            message: "Cannot verify API token"
          })
          next()
        }
      })
    } else {
      res.status(httpStatus.UNAUTHORIZED).json({
        error: true,
        message: "Provide Token"
      })
    }

  }

};