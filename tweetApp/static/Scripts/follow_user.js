const make_follow_request = async (event, userId) => {
    const button = event.target
    const request = await fetch(`http://127.0.0.1:8000/api/user/followers/add/${userId}`)
    const response = await request.json()

    console.log("FOLLOW APİ:", response)

    if (response.api_message.status === "eklendi") {

        button.innerText = "Takip Ediliyor"
        
    } else if (response.api_message.status === "çıkarıldı") {


        button.innerText = "Takip Et"
    }


}