#from pexc import OobException
import pexc

class HexCoordFactory:
    def __init__( self, mx, my ):
        self.mx = mx
        self.my = my
    def len( self ):
        return self.mx*self.my
    __len__ = len
    def cidx( self, i ):
        if type(i) == type(1):
            return i
        else: # list/tuple
            return self.AsIndex(i)
    def cxy( self, i ):
        if type(i) == type(1):
            x,y = self.AsPair( i )
        else:
            x,y = i[0],i[1]
        return (x,y)
    def CheckInBounds( self, i ):
        x,y = self.cxy(i)
        if x < 0 or x >= self.mx:
            raise pexc.OobException
        if y < 0 or y >= self.my:
            raise pexc.OobException
    #
    def AsIndex( self, p ):
        self.CheckInBounds(p)
        return p[1]*self.mx + p[0]
    def AsPair( self, i ):
        #self.CheckInBounds(i)
        y = i // self.mx
        x = i % self.mx
        return (x,y)
    def Direction1( self, i ):
        x,y = self.cxy( i )
        return self.AsIndex( ((x+y%2),(y-1)) )
    def Direction2( self, i ):
        x,y = self.cxy( i )
        return self.AsIndex( (x+1,y) )
    def Direction3( self, i ):
        x,y = self.cxy( i )
        return self.AsIndex( ((x+y%2),(y+1)) )
    def Direction4( self, i ):
        x,y = self.cxy( i )
        return self.AsIndex( ((x-1+y%2),(y+1)) )
    def Direction5( self, i ):
        x,y = self.cxy( i )
        return self.AsIndex( (x-1,y) )
    def Direction6( self, i ):
        x,y = self.cxy( i )
        return self.AsIndex( ((x-1+y%2),(y-1)) )
    def AbsRing1( self, i ):
        xy = self.cxy(i)
        t = []
        for fn in [self.Direction1,self.Direction2,self.Direction3,self.Direction4,self.Direction5,self.Direction6]:
            try:
                np = fn( xy )
                t.append( np )
            except pexc.OobException as e:
                t.append( None )
        return t
    def Ring1( self, i ):
        xy = self.cxy(i)
        t = set()
        for fn in [self.Direction1,self.Direction2,self.Direction3,self.Direction4,self.Direction5,self.Direction6]:
            try:
                np = fn( xy )
                t.add( np )
            except pexc.OobException as e:
                pass
        return t
    def Range1( self, i ):
        r1 = self.Ring1( i )
        r1.update( { self.cidx(i) } )
        return r1
    def Range2( self, i ):
        r1 = self.Ring1( i )
        r2 = set()
        for r in r1:
            r2.update( self.Ring1(r) )
        return r2
    def Ring2( self, i ):
        r0 = { self.cidx(i) }
        r1 = self.Ring1( i )
        r2 = self.Range2( i )
        r2.difference_update( r0 )
        r2.difference_update( r1 )
        return r2
    def Rangen( self, rng, i ):
        if rng == 2:
            return self.Range2( i )
        elif rng == 1:
            return self.Range1(i)
        elif rng < 1:
            return set()
        r1 = self.Rangen( rng - 1, i )
        r2 = set()
        for r in r1:
            r2.update( self.Ring1(r) )
        return r2
    def Ring( self, rng, i ):
        if rng == 1:
            return self.Ring1( i )
        r1 = self.Rangen( rng - 1, i )
        r2 = self.Rangen( rng, i )
        r2.difference_update( r1 )
        return r2
            

