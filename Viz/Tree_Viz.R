# Title     : Visualize ICMCTS
# Created by: jdfre


library(visNetwork)


processFile = function(filepath) {
  lines = NULL
  con = file(filepath, "r")
  while ( TRUE ) {
    line = readLines(con, n = 1)
    if ( length(line) == 0 ) {
      break
    }
    print(line)
    lines = c(lines, line)
  }

  close(con)
  return(lines)
}

assign_colors = function(node) {
  palette = colorRampPalette(colors=c("#FF0000", "#182848"))
  visits = sort(unique(node$value), decreasing = T)
  cols = palette(length(visits))

  idx = sapply(node$value, function(x) which(x == visits))

  color = cols[idx]
  return(color)
}

lines = processFile("../example_trees/test_tree4.txt")


lines = gsub("  *", " ", lines)
r = lines[1]
best.move = lines[startsWith(lines, "#")]
lines = lines[lines != ""]
lines = lines[!startsWith(lines, "#")]

lines = lines[-1]


# Process root
r.stats = unlist(strsplit(r, ": "))[2]
r.stats = gsub("\\]", "", r.stats)
r.stats = gsub(" ", "", r.stats)
r.stats = unlist(strsplit(r.stats, "/"))
r.stats = as.numeric(r.stats)

from = NULL
to = NULL
val = r.stats[2]


ROUND_DIGITS = 5

track = list(root = 0)



for(i in seq_along(lines)) {
  cont = unlist(strsplit(lines[i], "\\| "))

  cont = cont[cont != ""]
  info = unlist(strsplit(cont, "\\] "))

  t = gsub("\\[M:", "", unlist(strsplit(info[1], " "))[1])
  v = unlist(strsplit(info[1], "A: "))[2]
  v = as.numeric(unlist(strsplit(v, "/ ")))

  v = v[2]
  f = unlist(strsplit(info[2], " "))[1]
  f = unlist(strsplit(f, ":"))

  f = f[1]
  if(f == "None") {
    f = "root"
  }

  names(v) = t
  from = c(from, f)
  to = c(to, t)
  val = c(val, v)
}
names(val)[1] = "root"
val.names = names(val)
val = data.frame(val)
colnames(val)[1] = "value"
val$id = val.names

nodes = data.frame(id = unique(c(from, to)))
nodes$label = gsub("\\:.*", "", nodes$id)
nodes = merge(nodes, val, by = "id")
nodes$title = round(nodes$value, 4)
#nodes$value = val
edges = data.frame(from = from, to = to)

nodes$color = assign_colors(nodes)
visNetwork(nodes, edges) %>%
  visOptions(collapse = T, highlightNearest = T)






