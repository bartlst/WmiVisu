function showModal(modalID=null)
{
  if(modalID)
  {
    document.getElementById(modalID).classList.toggle('active')
    document.querySelector(".body__overlay").classList.toggle('active')
  }
  else{
    document.querySelector(".modal").classList.toggle('active')
    document.querySelector(".body__overlay").classList.toggle('active')
  }


}
