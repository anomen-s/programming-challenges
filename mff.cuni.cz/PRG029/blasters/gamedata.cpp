#include "gamedata.h"

#include "logger.h"
#include "net.h"

Player::Player()
{
   alive = false;
   ptype = PT_ABSTRACT;
   pid = 0;
   ping = 0;
   logger->log("constructing abstract player");
}

Player::Player(PlayerType type_, PID pid_, const char *name_, int score_)
{
	pid = pid_;
	ping = 0;
    ptype = type_;
	px = 0;
	py = 0;
	heading = RIGHT;
	moving = false;
	score = score_;
	switch (type_) {
	    case PT_REMOTE:
	        name = std::string(name_);
	        break;
		case PT_LOCAL1:
			pcontrols = &globals.p1controls;
			name = globals.player1;
			break;
		case PT_LOCAL2:
			pcontrols = &globals.p2controls;
			name = globals.player2;
			break;
		default:
			logger->log("ERROR: Invalid parameter in LocalPlayer constructor");
			break;
	}//switch
}

void Player::newRound(int maxbombs, float px, float py) 
{
    alive = true;
    bombing = false;
    heading = LEFT;
    moving = false;
    this->maxbombs = maxbombs;
    this->px = px;
    this->py = py;
    nobombtimeout = 0;
    bonusspeed = 0;
    bonusstrength = 0;
}

void Player::removePlayer()
{
 for(Connections::iterator c = gConnections.begin(); c != gConnections.end(); ++c) {
    if (c->pid == pid) {
        c->Close();
        gConnections.erase(c);
        break;
    }//if
 }//for
}

bool Player::localControls() const
{
    return ((ptype == PT_LOCAL1) || (ptype == PT_LOCAL2));
}		

Player::PlayerType Player::type() const
{ 
	return ptype; 
}

Player::~Player()
{

}

int Player::getMaxBombs()
{
    if (nobombtimeout > globals.getGameTimer()) {
        return 0;
    } else {
        return maxbombs;
    }//if/else
/*    for (PowerUps::iterator i = powerups.begin(); i != powerups.end(); ++i) {
        switch (i->type) {
            case POWER_NOBOMB:
                return 0;
            case POWER_BOMB:
                b++;
        }//switch
    } //for*/
}

void Player::setMaxBombs(int bombs)
{
    maxbombs = bombs;
}

void Player::pickupPowerUp(const PowerUp& pu)
{
    PowerUp puc;
    switch (pu.type) {
        case POWER_NOBOMB:   // player cannot cast bombs
            nobombtimeout = globals.getGameTimer() + pu.data;
            break;
        case POWER_STRENGTH: // bombs +1
            bonusstrength += pu.data;
            break;
        case POWER_BOMB:     // one more bomb
            maxbombs += pu.data;
            break;
        case POWER_SPEED:     // faster movement
            bonusspeed += (pu.data / STEP_PRECISION);
            break;
        default:
            logger->log("Invalid powerup: ", pu.type);
    }//switch
}

int Player::cellposx()
{
    return ftoi(px);
}
int Player::cellposy()
{
	return ftoi(py);
}
Position Player::cellpos()
{
 return Position(cellposx(), cellposy());
}

