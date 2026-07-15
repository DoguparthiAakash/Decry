import java.io.FileReader;
import java.math.BigInteger;
import java.util.*;
import com.google.gson.*;

public class ShamirSecret {

    static class Share {
        int x;
        BigInteger y;

        Share(int x, BigInteger y) {
            this.x = x;
            this.y = y;
        }
    }

    public static void main(String[] args) throws Exception {
        String[] files = {"test_case_1.json", "test_case_2.json"};
        for (String fileName : files) {
            System.out.println("Processing " + fileName + "...");
            processFile(fileName);
            System.out.println();
        }
    }

    private static void processFile(String fileName) throws Exception {
        JsonObject jsonObject = JsonParser.parseReader(new FileReader(fileName)).getAsJsonObject();
        JsonObject keys = jsonObject.getAsJsonObject("keys");

        int k = keys.get("k").getAsInt();

        List<Share> shares = new ArrayList<>();

        for (Map.Entry<String, JsonElement> entry : jsonObject.entrySet()) {
            if (entry.getKey().equals("keys")) continue;

            int x = Integer.parseInt(entry.getKey());
            JsonObject obj = entry.getValue().getAsJsonObject();

            int base = Integer.parseInt(obj.get("base").getAsString());
            String value = obj.get("value").getAsString();

            BigInteger y = new BigInteger(value, base);
            shares.add(new Share(x, y));
        }

        // Sort shares by x
        shares.sort(Comparator.comparingInt(s -> s.x));

        // Take first k shares
        List<Share> selected = shares.subList(0, k);

        BigInteger secret = lagrangeInterpolationAtZero(selected);

        System.out.println("Constant term (c) = " + secret);
    }

    private static BigInteger lagrangeInterpolationAtZero(List<Share> shares) {

        BigInteger sumNumerator = BigInteger.ZERO;
        BigInteger commonDenominator = BigInteger.ONE;

        // Calculate a common denominator to prevent precision loss during integer division
        for (int i = 0; i < shares.size(); i++) {
            BigInteger denominator = BigInteger.ONE;
            int xi = shares.get(i).x;
            for (int j = 0; j < shares.size(); j++) {
                if (i == j) continue;
                int xj = shares.get(j).x;
                denominator = denominator.multiply(BigInteger.valueOf(xi - xj));
            }
            commonDenominator = commonDenominator.multiply(denominator);
        }

        for (int i = 0; i < shares.size(); i++) {

            BigInteger numerator = BigInteger.ONE;
            BigInteger denominator = BigInteger.ONE;

            int xi = shares.get(i).x;

            for (int j = 0; j < shares.size(); j++) {
                if (i == j) continue;

                int xj = shares.get(j).x;

                numerator = numerator.multiply(BigInteger.valueOf(-xj));
                denominator = denominator.multiply(BigInteger.valueOf(xi - xj));
            }

            // Multiply the term by (commonDenominator / denominator) so we can do a single division at the end
            BigInteger termNumerator = shares.get(i).y.multiply(numerator).multiply(commonDenominator).divide(denominator);
            sumNumerator = sumNumerator.add(termNumerator);
        }

        return sumNumerator.divide(commonDenominator);
    }
}