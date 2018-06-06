package byog.Core.Nodes;

public class TileNode extends TileAC {

        /*
            Private custom class for storing important information.
            Will be useful for drawing hallways.
         */

    public TileNode(int xcor, int ycor) {
        //A small class to represent important nodes within a room.
        //Could be turned into its own class later on if we expand
        //the features of it.
        x = xcor;
        y = ycor;
    }

}
