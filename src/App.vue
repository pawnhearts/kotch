<template>
	<div id="chat">
        <message v-for="message in messages" v-bind:message="message" v-bind:key="message.count" v-bind:root="1"></message>
	</div>
</template>

<script>
import Message from './components/Message.vue'

export default {
	components: {
		Message
	},
    data: function(){
        return {
            messages: [],
            messages_by_count: {}
        }
    }
}
</script>

<style lang="css">

</style>