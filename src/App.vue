<template>
	<div id="body">
        <div id="messages">
            <message v-for="message in messages" v-bind:message="message" v-bind:key="message.count" v-bind:root="1"></message>
	    </div>
        <PostForm/>
	</div>
</template>

<script>
import Message from './components/Message.vue'
import PostForm from './components/PostForm.vue'

export default {
	components: {
		Message, PostForm
	},
    data: function(){
        return {
            messages: chat.messages,
            messages_by_count: chat.messages_by_count
        }
    }
}
</script>

<style lang="css">

</style>