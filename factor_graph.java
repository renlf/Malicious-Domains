package fg;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Iterator;
import java.util.Map;
import java.util.Map.Entry;
import java.util.Set;

public class FactorGroup {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		
		double bl_benign = 0.01;
		double wl_benign = 0.99;
		double unknown = 0.5;
		
		double bb = 0.75;
		double bm = 0.25;
		double mb = 0.49;
		double mm = 0.51;
		
		Set<String> black_list = new HashSet<>();
		Set<String> white_list = new HashSet<>();
		
		HashMap<String, Integer> dm_ht = new HashMap<String, Integer>();
		Set<String> conn = new HashSet<String>();
		Set<String> domain_host = new HashSet<String>();
		
		HashMap<Integer, Double> dhp_init = new HashMap<Integer, Double>();
		
		File bl_list = new File("black_list");
		try {
			
			InputStreamReader bl_reader = new InputStreamReader(new FileInputStream(bl_list));
			BufferedReader bl_br = new BufferedReader(bl_reader);
			String b_line = "";
			while ((b_line=bl_br.readLine())!=null) {
				black_list.add(b_line);
				
			}
			bl_br.close();
			
			
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
		File wl_list = new File("white_list");
		try {
			
			InputStreamReader wl_reader = new InputStreamReader(new FileInputStream(wl_list));
			BufferedReader wl_br = new BufferedReader(wl_reader);
			String wl_line = "";
			while ((wl_line=wl_br.readLine())!=null) {
				white_list.add(wl_line);
				
			}
			wl_br.close();
			
			
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
		File dm_file = new File("new_dns_data");
		try {
			
			InputStreamReader dm_reader = new InputStreamReader(new FileInputStream(dm_file));
			BufferedReader dm_br = new BufferedReader(dm_reader);
			String dm_line = "";
			while ((dm_line=dm_br.readLine())!=null) {
				
				String[] dh = dm_line.split(" ");
				if(dh.length==2)
				{
					domain_host.add(dh[0]);
					domain_host.add(dh[1]);
					conn.add(dm_line);
				}
				
			}
			System.out.println(domain_host.size());
			dm_br.close();
			
			
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
		File id_out = new File("id_out");
		try {
			BufferedWriter id_writer = new BufferedWriter(new FileWriter(id_out));
			
			Iterator<String> it_dh = domain_host.iterator();
			int id = 0;
			while (it_dh.hasNext()) {
				String tmp_dh = (String) it_dh.next();
				dm_ht.put(tmp_dh, id);
				if (black_list.contains(tmp_dh)) {
					dhp_init.put(id, bl_benign);
					black_list.remove(tmp_dh);
				}
				else if(white_list.contains(tmp_dh))
				{
					dhp_init.put(id, wl_benign);
					white_list.remove(tmp_dh);
				}
				else {
					dhp_init.put(id, unknown);
				}
				
				id_writer.write(id + " " + tmp_dh + "\n");
				id++;
				//System.out.println(id);

			}
		} catch (IOException e1) {
			// TODO Auto-generated catch block
			e1.printStackTrace();
		}
		
		
		int total_factor = dm_ht.size() + conn.size();
	
		System.out.println(total_factor);
		
		File fg_file = new File("dns.fg");
		try {
			BufferedWriter out = new BufferedWriter(new FileWriter(fg_file));
			out.write(total_factor + "\n" + "\n");
			
			Iterator<Entry<Integer, Double>> dh_it = dhp_init.entrySet().iterator();
			int i=0;
			while (dh_it.hasNext()) {
				Map.Entry<Integer, Double> entry= dh_it.next();
				int tmp_id = entry.getKey();
				double tmp_mlp = entry.getValue();
				
				out.write(1+"\n");
				out.write(tmp_id+"\n");
				out.write(2+"\n");
				out.write(2+"\n");
				out.write(0 + " " + tmp_mlp + "\n");
				out.write(1 + " " + (double)(Math.round((1.0-tmp_mlp)*100)/100.0) + "\n");
				out.write("\n");
//				if(tmp_mlp == 0.01)
//					System.out.println(1);
				i++;

			}
			
			System.out.println(dm_ht.size() + " " + i + "\n");
			
			Iterator<String> it = conn.iterator();
//			i=0;
			while (it.hasNext()) {
				String[] tmp_conn = it.next().split(" ");
				String domain ="";
				String host = "";
				if (tmp_conn.length == 2) {
					host = tmp_conn[0];
					domain = tmp_conn[1];
					
					int host_id = dm_ht.get(host);
					int domain_id = dm_ht.get(domain);
					
					out.write(2+"\n");
					out.write(host_id + " " + domain_id +"\n");
					out.write(2 + " " + 2 + "\n") ;
					out.write(4 + "\n");
					out.write(0 + " " + bb + "\n");
					out.write(1 + " " + bm + "\n");
					out.write(2 + " " + mb + "\n");
					out.write(3 + " " + mm + "\n");
					out.write("\n");
					i++;
				}
				
			}
			out.close();
			System.out.println(conn.size() + " " + i + "\n");
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		//dm_ht.addAll(conn);
	}

}
