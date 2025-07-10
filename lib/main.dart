import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

void main() {
  runApp(OITrackerApp());
}

class OITrackerApp extends StatelessWidget {
  const OITrackerApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Nifty OI Tracker',
      theme: ThemeData(primarySwatch: Colors.deepPurple),
      home: HomePage(),
    );
  }
}

class HomePage extends StatefulWidget {
  const HomePage({super.key});

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  TextEditingController fromController = TextEditingController(text: "09:20");
  TextEditingController toController = TextEditingController(text: "11:00");

  List<dynamic> oiData = [];

  Future<void> fetchOIData() async {
    final from = fromController.text;
    final to = toController.text;
    final url = Uri.parse('http://127.0.0.1:5000/data?from=$from&to=$to');

    try {
      final response = await http.get(url);

      if (response.statusCode == 200) {
        final List<dynamic> data = json.decode(response.body);
        setState(() {
          oiData = data;
        });
      } else {
        throw Exception('Failed to load OI data');
      }
    } catch (e) {
      print("Error: $e");
      ScaffoldMessenger.of(
        context,
      ).showSnackBar(SnackBar(content: Text("Error fetching data")));
    }
  }

  Widget buildOIList() {
    if (oiData.isEmpty) {
      return Center(child: Text("No data to show"));
    }

    return ListView.builder(
      itemCount: oiData.length,
      itemBuilder: (context, index) {
        final item = oiData[index];
        return ListTile(
          title: Text("Strike: ${item['strike']}"),
          subtitle: Text(
            "Call OI: ${item['call_oi']} | Put OI: ${item['put_oi']}",
          ),
        );
      },
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Nifty OI Tracker')),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: [
            Row(
              children: [
                Expanded(
                  child: TextField(
                    controller: fromController,
                    decoration: InputDecoration(labelText: 'From (HH:MM)'),
                  ),
                ),
                SizedBox(width: 16),
                Expanded(
                  child: TextField(
                    controller: toController,
                    decoration: InputDecoration(labelText: 'To (HH:MM)'),
                  ),
                ),
                SizedBox(width: 16),
                ElevatedButton(onPressed: fetchOIData, child: Text('Get')),
              ],
            ),
            SizedBox(height: 20),
            Expanded(child: buildOIList()),
          ],
        ),
      ),
    );
  }
}
