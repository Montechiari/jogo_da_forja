import Head from 'next/head'

const Home = () => (
  <div className="container">
    <Head>
      <title>Jogo da Forja</title>
      <link rel="icon" href="/favicon.ico" />
    </Head>
      <div id="advantage">advantage</div>
      <div className="display">
        <div className="players-box">
            <div className="a-player" id="player1">
                <div id="player-stats-bar">
                    <div className="info-strip" id="name-strip">
                        <div className="sub-header">name</div>
                        <div className="sub-header">weapon</div>
                    </div>
                    <div className="info-strip" id="hp-strip">hp bar</div>
                    <div className="info-strip" id="ap-strip">ap bar</div>
                </div>
            </div>
            <div className="a-player" id="player2">
                <div id="player-stats-bar">
                <div className="info-strip" id="header-strip">
                    <div className="sub-header">name</div>
                    <div className="sub-header">weapon</div>
                </div>
                <div className="info-strip" id="hp-strip">hp bar</div>
                <div className="info-strip" id="ap-strip">ap bar</div>
                </div>
            </div>
        </div>
        <div className="text-box">TEXT BOX</div>
      </div>
      <div className="action-bar">
         <div className="game-interface" id="actions">ACTIONS</div>
         <div className="game-interface" id="confirm">CONFIRM</div>
      </div>

  </div>
)

export default Home
