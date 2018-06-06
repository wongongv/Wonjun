package byog.Core.Nodes;

import byog.TileEngine.TETile;

public abstract class TileAC implements Tile {

    protected int x;
    protected int y;
    protected TETile look;

    public int[] getcoords() {
        return new int[] {x, y};
    }

    public int getx() {
        return x;
    }

    public int gety() {
        return y;
    }

    public void changelook(TETile newt) {
        look = newt;
    }

    public TETile getLook() {
        return look;
    }

    public void setCoords(int xc, int yc) {
        x = xc;
        y = yc;
    }
}
