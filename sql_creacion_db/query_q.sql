use proyectos;
select nombre, descripcion, fase, segundos, creation_time, update_time 
from recursos, Proyectos, fases, Cargas 
where recursos.Idrecurso=Cargas.IdRecurso 
and Proyectos.idProyecto=Cargas.idProyecto 
and fases.idfase = Cargas.idfase
order by Cargas.IdRecurso; 