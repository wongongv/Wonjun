package byog.Core.Nodes;

public class Portal extends TileAC {

    private Portal partner;

    public Portal(int xc, int yc, Portal p) {
        x = xc;
        y = yc;
        partner = p;
    }

    public Portal() {
        x = 0;
        y = 0;
        partner = this;
    }

    public Portal pcoords() {
        return partner;
    }


    public void setpart(Portal x) {
        partner = x;
    }

    public boolean isme(int[] coords) {
        return (coords[0] == x && coords[1] == y);
    }

}
