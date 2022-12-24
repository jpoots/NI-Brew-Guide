document.addEventListener('DOMContentLoaded', function() {


    if(document.querySelectorAll('.pagerChanger')){
        pagination()
    }

    if(document.getElementById('contactForm')){
        contactValidation()
    }

    if(document.getElementById('locationForm')){
        geoLocate()
    }

    if(document.getElementById('review')){
        let text = document.getElementById('text')
        let charCount = 100
        let charRemain = document.getElementById('charCount')

        charLimit(text, charCount, charRemain)
        review()
    }
})


function pagination() {

    window.history.replaceState(null, null, window.location.href);
      
    let pageChangers = document.querySelectorAll('.pageChanger')

    pageChangers.forEach(btn => {
        btn.addEventListener('click', () => document.getElementById(`${btn.innerHTML}`).submit())
    })
}


function contactValidation(){

    let form = document.getElementById('contactForm')
    let charRemain = document.getElementById('charCount')
    let charCount = 500
    let email = document.getElementById('email')
    let text = document.getElementById('body')
    
    charLimit(text, charCount, charRemain)

    form.addEventListener('submit', (event) => {

        if(text.value.length == 0){
            event.preventDefault()
        }

        if(document.getElementById('name').value.length == 0){
            event.preventDefault()
        }

        if(!email.value.includes('@') || !email.value.includes('.') || email.value.trimEnd().includes(' ') || email.value.length == 0){
            event.preventDefault()
        }
    })
}


function geoLocate(){
    document.getElementById('locationSubmit').addEventListener('click', () => {

        navigator.geolocation.getCurrentPosition((position) => {
            document.getElementById('long').value = position.coords.longitude
            document.getElementById('lat').value = position.coords.latitude
            document.getElementById('locationForm').submit()
        }, () => {
            alert("Please allow location for personalised results")
        })
    })
}


function charLimit(text, charCount, charRemain){

    text.addEventListener('input', (e) => {
        if(e.data != null) {
            charCount -= 1
            charRemain.innerHTML = charCount
        }

        else{
            charCount += 1
            charRemain.innerHTML = charCount
        }
    })
}


function review(){
    form = document.getElementById('review')
    textbox = document.getElementById('text')

    form.addEventListener('submit', (event) => {
        if(!document.getElementById('text')){
            event.preventDefault()
        }
        const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value
        fetch('/review/', {
            method:'POST',
            headers: {'X-CSRFToken': csrftoken},
            mode: 'same-origin',
            body: JSON.stringify({
                review: textbox.value,
                shopId: document.getElementById('shop').innerHTML
            })
        })
        .then(response =>{

            if(response.status === 201){

                contentElement = document.createElement('div')
                contentElement.setAttribute("class", "content")
                contentElement.innerHTML = textbox.value

                authorElement = document.createElement('div')
                authorElement.setAttribute('class', 'author')
                authorElement.innerHTML = document.getElementById('hiddenUsername').innerHTML

                nowElement = document.createElement('div')
                nowElement.setAttribute('class', 'timestamp')
                nowElement.innerHTML = "Just now"

                reviewElement = document.createElement('div')
                reviewElement.setAttribute('class', 'review')
                reviewElement.append(contentElement)
                reviewElement.append(authorElement)
                reviewElement.append(nowElement)


                document.getElementById('reviews').prepend(reviewElement)
                document.getElementById('charCount').innerHTML = 100
                textbox.value = ''

                // add review to page
            }
            else{
                console.log(response.status)
            }
        }

        )
        event.preventDefault()
    })
}
