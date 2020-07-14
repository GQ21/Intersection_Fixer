import maya.cmds as mc
import numpy as np

def distance_check(line,point):
    """Check whether lines end or start point is closer to the given point"""    
    line_start = line[0]    
    line_end = line[1]
    d1 = np.sqrt(
      (point[0] - line_start[0])
      * (point[0] - line_start[0])
      + (point[1] - line_start[1])
      * (point[1] - line_start[1])
      + (point[2] - line_start[2])
      * (point[2] - line_start[2])
      )
    d2 = np.sqrt(
      (point[0] - line_end[0])
      * (point[0] - line_end[0])
      + (point[1] - line_end[1])
      * (point[1] - line_end[1])
      + (point[2] - line_end[2])
      * (point[2] - line_end[2])
    )
    if d1 < d2:
        return 0
    else:
        return 1    
        
def find_intersection(polygon,vertex_count,line):
    """Check whether line intersects with polygon"""
    angle = 0
    result = False     

    #Points in Edge 
    P0 = line[0]
    P1 = line[1] 

    #Points in Plane
    Q0 = polygon[0]
    Q1 = polygon[1]
    Q2 = polygon[2]

    #vectors in Plane
    q1 = np.subtract(Q1,Q0)
    q2 = np.subtract(Q2,Q0)

    #vector normal to Plane
    n = np.cross(q1, q2)/np.linalg.norm(np.cross(q1, q2))
    
    #Edge direction vector 
    u = np.subtract(P0,P1)
    #Vector from plane ref point to edge ref point
    w = np.subtract(P0,Q0) 

    original_distance = -1 * np.dot(n, Q0)     
    distance1 = np.dot(n,P0) + original_distance
    distance2 = np.dot(n,P1) + original_distance         
     
    if distance1 * distance2 >= 0:        
        result = False              
    else:
        magnitude = np.sqrt(np.dot(u, u))        
        u = np.divide(u,magnitude)          
        numerator = -1 * (np.dot(n, P0) + original_distance)        
        denominator = np.dot(n, u)

        if denominator == 0:
            intersection = P0
        else:
            dist = numerator / denominator            
            point = np.add(P0, np.dot(u, dist))            
            intersection = point            
        for i in range(vertex_count):
            Q0 = polygon[i]
            Q2 = polygon[(i+1)%vertex_count] 

            a = np.subtract(Q0,intersection)
            b = np.subtract(Q2,intersection)

            dot_product = np.dot(a,b)
            vector_magnitude = np.sqrt(np.dot(a,a)) *  np.sqrt(np.dot(b,b))
            if vector_magnitude != 0:
                temp_angle = np.arccos(dot_product / vector_magnitude) 
                angle = angle + temp_angle
                
        if angle >= 6.2831852443477334051294219973061:            
            result = True, point       
    return result

def face_to_vtxs(face):
    """Exctract vertices from given face"""
    face_name = face.split('.')[0]
    edges = mc.polyInfo(face, fe=True)[0].split()[2:]    
    edges_vtxs= []  
      
    for e in edges:
        vtxs = mc.polyInfo(str(face_name + '.e[' + e + ']'), ev=True)[0].split()[1:4]
        edges_vtxs.append(vtxs)
        
    return edges_vtxs  

def intersection(offset=None):
    """Go through polygons and check if there are intersections"""
    if len(mc.ls(sl = True, o = True)) > 1:
        mc.error('Please select only one Mesh')
    elif len(mc.ls(sl = True, o = True)) == 0:
        mc.error('Please select mesh')
    else:
        faces = mc.ls(
            mc.polyListComponentConversion(
                mc.ls(sl=True,fl=True),
                tf = True
            ),
            fl = True
        )
        intersect_faces = []        
        obj_name = faces[0].split('.')[0] 
        i=0

        if len(faces) >= 1000:
            confirm_switch = mc.confirmDialog(
                    title = 'Warning',
                    message ='You selected over 1000 faces, which can take some time to proceed',
                    button=['Continue','Cancel'],
                    defaultButton = 'Continue',
                    cancelButton='Cancel',
                    dismissString = 'Cancel'
            )
            if confirm_switch == 'Continue':
                pass
            else:
                return 

        mc.progressWindow(
            title = 'Find intersecting faces',
            progress = 0,
            status = "Progressing:",
            min = 0,
            max = len(faces),
            isInterruptable = False
        )
        while len(faces) != 1:  
            mc.progressWindow(e = True, progress = i)    
            intersect = 0       
            vtx_ids = mc.polyInfo(faces[0], fv=True)[0].split()[2:]    
            vtx_count = len(mc.polyInfo(faces[0], fv=True)[0].split())-2     
            polygon = []
             
            for id in vtx_ids:
                polygon.append(mc.pointPosition(str(obj_name + '.vtx[' + id + ']'))) 

            base_edges_vtxs = face_to_vtxs(faces[0])
            polygon_const = polygon
            base_edges_vtxs_const = base_edges_vtxs
            vtx_count_const =  vtx_count
            
            for next_face in faces[1:]:        
                polygon = polygon_const
                base_edges_vtxs = base_edges_vtxs_const
                vtx_count =  vtx_count_const        
                
                next_edges_vtxs = face_to_vtxs(next_face)       
                next_edges = mc.polyInfo(next_face, fe=True)[0].split()[2:]
                shared_edges = []  
                
                for b in base_edges_vtxs:
                    for n in next_edges_vtxs:
                        if n[1] in b or n[2] in b:
                            shared_edges.append(n[0][:n[0].find(':')])

                edges = list(set(next_edges) - set(shared_edges))

                if len(edges)>0:
                    for e in edges:                
                        line_vtxs = mc.polyInfo(str(obj_name + '.e['+ e +']'), ev=True)[0].split()[2:]
                        line = []                                
                        line_start = mc.pointPosition(str(obj_name + '.vtx[' + line_vtxs[0] + ']'))
                        line_end = mc.pointPosition(str(obj_name + '.vtx[' + line_vtxs[1] + ']'))
                        line.append(line_start)
                        line.append(line_end)
                        
                        #find intersecion and if there is move edge points accordingly
                        intersection = find_intersection(polygon,vtx_count,line)                          
                        if intersection:
                            if not offset == None:
                                #get edge point which is closest to the intersection 
                                if distance_check(line, intersection[1]) == 0:
                                    #find vector between edge point and intersection
                                    c1 = np.subtract(line_end, intersection[1])
                                    #find offset point
                                    P2 = np.add(intersection[1], np.divide(c1,offset))                        
                                    #Move edge point into offset point cordinates                   
                                    mc.xform(str(obj_name + '.vtx[' + line_vtxs[0] + ']'), translation = P2)                        
                                else:                        
                                    c1 = np.subtract(line_start, intersection[1])                        
                                    P2 = np.add(intersection[1], np.divide(c1,offset))                                       
                                    mc.xform(str(obj_name + '.vtx[' + line_vtxs[1] + ']'), translation = P2)                                        
                                                                
                            intersect_faces.append(next_face)
                            intersect_faces.append(faces[0])
                            intersect = 1                             

                vtx_ids = mc.polyInfo(next_face, fv=True)[0].split()[2:]
                vtx_count = len(mc.polyInfo(next_face, fv=True)[0].split())-2         
                polygon = []    

                for id in vtx_ids:
                    polygon.append(mc.pointPosition(str(obj_name + '.vtx[' + id +']')))

                base_edges_vtxs = face_to_vtxs(next_face)                  
                next_edges = mc.polyInfo(faces[0], fe=True)[0].split()[2:]
                shared_edges = []  
                                
                for b in base_edges_vtxs:
                    for n in next_edges_vtxs:                               
                        if n[1] in b or n[2] in b:                                                                             
                            shared_edges.append(n[0][:n[0].find(':')])             

                edges = list(set(next_edges) - set(shared_edges))

                if len(edges)>0:
                    for e in edges:                
                        line_vtxs = mc.polyInfo(str(obj_name + '.e['+ e +']'), ev=True)[0].split()[2:]
                        line = []                                
                        line_start = mc.pointPosition(str(obj_name + '.vtx[' + line_vtxs[0] + ']'))
                        line_end = mc.pointPosition(str(obj_name + '.vtx[' + line_vtxs[1] + ']'))
                        line.append(line_start)
                        line.append(line_end) 
                        
                        intersection =  find_intersection(polygon,vtx_count,line)                                 
                        if intersection:    
                            if not offset == None:                  
                                if distance_check(line,intersection[1]) == 0:                        
                                    c1 = np.subtract(line_end, intersection[1])                        
                                    P2 = np.add(intersection[1], np.divide(c1,offset)) 
                                    mc.xform(str(obj_name + '.vtx[' + line_vtxs[0] + ']'), translation = P2)                                       
                                else:                        
                                    c1 = np.subtract(line_start, intersection[1])                        
                                    P2 = np.add(intersection[1], np.divide(c1,offset))                            
                                    mc.xform(str(obj_name + '.vtx[' + line_vtxs[1] + ']'), translation = P2)                                                                               
                            intersect_faces.append(next_face)
                            intersect_faces.append(faces[0])                                                                
            i=i+1
            faces = faces[1:]  
        mc.progressWindow(endProgress = True)
        mc.select(intersect_faces)







  
    