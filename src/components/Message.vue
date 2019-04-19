<template>
    <div v-bind:class="'message '+(replying?'replying':'')">
        <div v-show="replying">Replying...</div>
        <div style="margin-left:100px">
            <message v-for="message in reply_to" v-bind:message="message" v-bind:key="message.count"
                     v-if="root"></message>
        </div>
        {{ message.datetime|formatDate }} {{ message.count }} {{ message.ident }}
        <div class="header"><img v-bind:src="'/static/icons/countries/'+message.country.split('-')[0]+'.png'"><img
                v-if="message.country.indexOf('-') !== -1"
                v-bind:src="'/static/icons/countries/'+message.country+'.png'">{{ message.name }}
        </div>
        <div class="body">{{ message.body }}</div>
        <div v-if="message.file">
            <img v-bind:src="'/static/uploads/'+message.file">
        </div>
        <button @click="reply(message)">reply</button>
        <button @click="ignore(message)">ignore</button>
    </div>
</template>

<script>

    export default {
        props: ['message', 'root'],
        computed: {
            reply_to: function () {
                if (!this.message.reply_to) return []
                return this.message.reply_to.map(function (count) {
                    return chat.messages_by_count[count]
                })
            }
        },
        data: function () {
            return {
                replying: false
            }
        },
        methods: {
            reply: function (message) {
                this.$root.$emit('replying');
                this.replying = true;
                document.getElementById('reply_to').value = message.count;
            },
            ignore: function (message) {

            }
        },
        mounted: function () {
            this.$root.$on('replying', () => {
                this.replying = false;
            })
        }
    }
</script>