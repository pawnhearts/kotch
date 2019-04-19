<template>

<form id="post-form" @submit.prevent="post()">

        <div class="container">
            <p v-if="errors.length">
                <b>Please correct the following error(s):</b>
            <ul>
                <li v-for="error in errors">{{ error }}</li>
            </ul>
            </p>
            <input type="file" id="file" ref="file" v-on:change="handleFileUpload()"/>
            <input name="reply_to" id="reply_to" v-model="reply_to">
            <input name="icon" v-model="icon">
            <input name="name" v-model="name">
            <textarea name="body" id="body" v-model="body"></textarea>
            <button v-on:click="post()">Submit</button>
        </div>
</form>
</template>

<script>
    import axios from 'axios'
    export default {
        name: 'postform',
        data() {
            return {
                errors: [],
                name: '',
                icon: '',
                reply_to: '',
                body: '',
                file: ''
            }
        },

        methods: {
            post() {
                let form = document.getElementById('post-form');
                let formData = new FormData(form);


                if(this.file) {
                    formData.append('file', this.file);
                }

                const options = {
                  method: 'POST',
                  headers: { 'content-type': 'application/x-www-form-urlencoded' },
                  data: formData,
                  url: '/post'
                };
                axios(options).then(() => {
                    this.errors = [];
                }).catch((error) => {
                    this.errors = [];
                    console.log(error.response.data.error)
                    for(let k in error.response.data.error) {
                        this.errors.push(k+': '+error.response.data.error[k])
                    }
                });
                return false;
            },
            handleFileUpload() {
                this.file = this.$refs.file.files[0];
            }
        }
    }
</script>