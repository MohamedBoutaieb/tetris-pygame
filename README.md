# tetris-pygame
<h1> How to play </h1>
 clone the project and execute the script tetris.py with a python compiler 
<h2> Controls <h2>
<ul>
  <li>left arrow : move the block left  </li>
  <li>right arrow : move the block to the right  </li>
  <li> down : speed up </li>
  <li> up : make the block fall into its place</li>
  <li> x : rotate </li>
  <li> h : shadow assistance </li>
  <li> p :pause </li>
  </ul>
<h2> Score <h2>
  <table> <th>level  </th> <th> points for 1 line </th> <th> points for 2 lines </th> <th> points for 3 lines </th> <th> points for 4 lines </th>
<tr> <td>1 </td><td> 40 </td><td> 100 </td><td> 300 </td><td>400 </td> </tr>
    <tr><td>2 </td><td>80 </td><td> 200 </td><td> 600 </td><td> 800</td></tr>
<tr><td>k </td><td> k*40 </td><td> k*100 </td><td> k*200 </td><td> k*400</td></tr>
<tr><td>10 </td><td> 400 </td><td> 1000</td><td> 2000 </td><td> 4000</td></tr>
  </table>

<h2> About the game </h2>
The game board can be percieved this way :

  ![](/example.png)
Each sell of the board contains either None or a tuple containing the rgb color for the block after landing on its final position.
Each time you land a block , the cells content will be replaced by its respective rgb color tuple and you will get a new block in hand.
The white cells on the side exist to verify the possibility of a rotation or a translation on the sides , if a piece or a part of it have coordinates that correspond to these white boundaries , the movement is not possible and is automatically canceled .
  <h5> Are the new blocks totally random ? </h5>
  To avoid having 5 consecutive blocks of the same kind , the new blocks are randomly chosen from a bag containing all the 7 blocks , each time a piece is chosen, it's 
 discarded from the bag until all pieces are discarded then it's refilled again .

The fps was initially shown to demonstrate a smooth tetris exeperience but the smooth movement ( 1 pixel at a time instead of 1 cell at time) doesn't allow some critical movements :
 ![](/example2.png)
