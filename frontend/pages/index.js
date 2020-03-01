import Head from 'next/head'
import action1 from "../assets/ac1.png";
import action2 from "../assets/ac2.png";
import action3 from "../assets/ac3.png";
import action4 from "../assets/ac4.png";
import action5 from "../assets/ac5.png";
import action6 from "../assets/ac6.png";

const actionPictureDiameter= "86";

const Home = () => (
  <div className="container">
    <Head>
      <title>Jogo da Forja</title>
      <link rel="icon" href="/favicon.ico" />
      <style>
      @import url('https://fonts.googleapis.com/css?family=IBM+Plex+Mono&display=swap');
      @import url('https://fonts.googleapis.com/css?family=VT323&display=swap');
      </style>
    </Head>
    <div id="top-margin-bar"></div>
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
        <div className="text-box">
            <p>This is the area where the flavor text will be displayed. 1 2 3 @!#</p>
        </div>
      </div>
      <div className="action-bar">
        <div className="game-interface" id="actions">
                <div>
                    <img className="button-image" id="offensive-movement" src={action1} alt="stance1" width={actionPictureDiameter} height={actionPictureDiameter}/>
                </div>
                <div>
                    <img className="button-image" id="defensive-movement" src={action2} alt="stance2" width={actionPictureDiameter} height={actionPictureDiameter}/>
                </div>
                <div>
                    <img className="button-image" id="slash-attack" src={action3} alt="stance3" width={actionPictureDiameter} height={actionPictureDiameter}/>
                </div>
                <div>
                    <img className="button-image" id="thrust-attack" src={action4} alt="stance4" width={actionPictureDiameter} height={actionPictureDiameter}/>
                </div>
                <div>
                    <img className="button-image" id="slash-defense" src={action5} alt="stance5" width={actionPictureDiameter} height={actionPictureDiameter}/>
                </div>
                <div>
                    <img className="button-image" id="thrust-defense" src={action6} alt="stance6" width={actionPictureDiameter} height={actionPictureDiameter}/>
                </div>
        </div>
         <div className="game-interface" id="right-bar">
             <div>Turn: 666</div>
             <div>Confirm?</div>
             <div>
                    <div>V</div>
                    <div>X</div>
             </div>
         </div>
      </div>
      <div id="foot"></div>
  </div>
)

export default Home
