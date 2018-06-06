package byog.Core.Nodes;

public class Player extends TileAC {

    private int walleater;
    private int pvision;
    private int walks;
    public Player(int xc, int yc, int walks) {
        this.walks = walks;
        x = xc;
        y = yc;
        walleater = 0;
        pvision = 5;

    }

    public void move(char option) {
        //eliminates half the cases.
        option = Character.toLowerCase(option);
        //Utilizes the pre-built setCoords method in all TileNodes.
        switch (option) {
            case 'a':
                setCoords(x - 1, y);
                break;
            case 's':
                setCoords(x, y - 1);
                break;
            case 'd':
                setCoords(x + 1, y);
                break;
            case 'w':
                setCoords(x, y + 1);
                break;
            default :
                break;
        }
    }

    public boolean caneat() {
        return walleater > 0;
    }

    public void eattick() {
        if (walleater > 0) {
            walleater--;
        }
    }

    public void raisetick(int x) {
        walleater += x;
    }

    public void teleport(int[] coords) {
        setCoords(coords[0], coords[1]);
    }

    public int vision() {
        return pvision;
    }

    public void raisevis() {
        pvision++;
    }

    public void pluswalks(int n) {
        walks = walks + n;
    }
    public void minuswalks() {
        walks = walks - 1;
    }
    public int getwalks() {
        return walks;
    }

    public int getWalleater() {
        return walleater;
    }
}
