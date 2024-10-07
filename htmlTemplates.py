css = '''
<style>
.chat-message {
    padding: 2.5rem;
    border-radius: 1.5rem;
    margin-bottom: 1rem;
    display: flex;
    position: relative; /* Added position relative */
}

.chat-message.user {
    background-color: #2b313e;
}

.chat-message.bot {
    background-color: #475063;
}

.chat-message .avatar {
    width: 20%;
}

.chat-message .avatar img {
    max-width: 78px;
    max-height: 78px;
    border-radius: 20%;
    object-fit: scale-down;
}

.chat-message .message {
    width: 90%;
    padding: 0 1rem;
    color: #fff;
}

.small-font {
    font-size:16px !important;
    color: grey !important;
}

.css-pxxe24 {
    visibility: hidden;
}


</style>
'''

bot_template = '''
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css">
<div class="chat-message bot">
    <div class="avatar">
        <img src="https://www.kroger.com/content/v2/binary/image/pr/free-membership/imageset_simplify-your-shopping--3977085_22_p8w2_lp_loyaltyrewards_te_c_shoponline_dsk_416x312.png">
    </div>
    <div class="message">{{MSG}}</div>
</div>
'''

user_template = '''
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css">
<div class="chat-message user">
    <div class="avatar">
        <img src="https://www.kroger.com/content/v2/binary/image/pr/free-membership/imageset_personalized-savings--3977085_22_p8w2_lp_loyaltyrewards_te_b_savings_dsk_416x312.png">
    </div>
    <div class="message">{{MSG}}</div>
</div>

'''
