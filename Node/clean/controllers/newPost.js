module.exports=(req,res)=>{
    
  if(req.session.userID){  
    return res.render('create')
  }

  res.redirect('/auth/login')
}


