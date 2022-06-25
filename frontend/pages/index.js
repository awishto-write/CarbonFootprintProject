import Head from 'next/head'
import Image from 'next/image'
import styles from '../styles/Home.module.css'

export default function Home() {
  return (
    <div className={styles.container}>
      <Head>
        <title>Create Next App</title>
        <meta name="description" content="Generated by create next app" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <h2 className="login">Login</h2>
      <input />
      <br></br>
      <input />

      <div>
        <button>Login</button>
      </div>
      <a href="#">Not a member yet? Sign up here.</a>
    </div>
  )
}