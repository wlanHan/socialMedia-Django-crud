const make_api_request = async (event, tweetId) => {

    const request = await fetch(`http://127.0.0.1:8000/api/tweet/${tweetId}/begen`)
    const response = await request.json()

    const heartIcon = event.target
    const likeCount = heartIcon.nextElementSibling
 
    if (response.api_message.status === "Like Eklendi") {

        // kalp ikonu güncelle 
        // sayacı güncelle
        heartIcon.name = "heart-sharp"
        likeCount.innerText = response.api_message.total_likes

    } else if (response.api_message.status === "Unlike Yapıldı") {

        heartIcon.name = "heart-outline"
        likeCount.innerText = response.api_message.total_likes
    } else {

      alert("Bir hata meydana geldi lütfen daha sonra tekrar dene.")
    }

    console.log("API DAN GELEN RESPONSE:", response)
}